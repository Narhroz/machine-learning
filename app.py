"""StayCheck - beranda + prediksi pembatalan booking hotel (Streamlit)."""
import streamlit as st
from ui import inject_css, top_nav, html, team_html, BRAND
from utils import (require_artifact, known_countries, validate_inputs, predict, cancel_rate_pct,
                   COUNTRY_NAMES, OTHER_COUNTRY, SEGMENT_LABELS, CUSTOMER_LABELS,
                   LEAD_MIN, REQ_MIN, REQ_MAX)

st.set_page_config(page_title=f"{BRAND} - Prediksi pembatalan booking hotel", page_icon="🏨", layout="wide")
inject_css()
artifact = require_artifact()
countries = known_countries(artifact)
country_options = countries + [OTHER_COUNTRY]
country_fmt = lambda c: "Negara lain" if c == OTHER_COUNTRY else f"{COUNTRY_NAMES.get(c, c)} ({c})"
metrics = artifact.get("metrics_test", {})
thr = artifact["threshold"]

DEFAULTS = {"in_lead": 60, "in_country": "PRT" if "PRT" in countries else countries[0],
            "in_segment": "Online TA", "in_requests": 0, "in_customer": "Transient"}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)

PRESETS = {
    "Pesan online jauh hari": {"in_lead": 200, "in_country": "PRT", "in_segment": "Online TA",
                               "in_requests": 0, "in_customer": "Transient"},
    "Tamu perusahaan, mepet": {"in_lead": 3, "in_country": "GBR", "in_segment": "Corporate",
                               "in_requests": 2, "in_customer": "Contract"},
    "Liburan keluarga": {"in_lead": 45, "in_country": "DEU", "in_segment": "Direct",
                         "in_requests": 2, "in_customer": "Transient-Party"},
}


def clear_result():
    st.session_state.pop("result", None)


def apply_preset(name):
    for k, v in PRESETS[name].items():
        if k == "in_country" and v not in country_options:
            v = OTHER_COUNTRY
        st.session_state[k] = v
    clear_result()


def reset_form():  # FR-09
    for k, v in DEFAULTS.items():
        st.session_state[k] = v
    clear_result()


def lead_human(d):
    if d == 0:
        return "Dipesan di hari yang sama dengan kedatangan."
    if d < 7:
        return f"Dipesan {d} hari sebelum kedatangan (mepet)."
    if d < 30:
        return f"Dipesan sekitar {round(d/7)} minggu sebelum kedatangan."
    if d < 365:
        return f"Dipesan sekitar {round(d/30)} bulan sebelum kedatangan."
    return "Dipesan sekitar setahun sebelum kedatangan."


# ------------------------------------------------------------------ nav + hero
top_nav()
rate = cancel_rate_pct()
dots = "".join('<i class="on"></i>' if i < round(rate) else "<i></i>" for i in range(100))
html(f"""
<section class="hero">
<div>
<h1>Booking ini bakal batal nggak, ya?</h1>
<p class="lead">{BRAND} membaca pola dari puluhan ribu reservasi hotel untuk memperkirakan peluang sebuah booking dibatalkan. Isi lima info, jawabannya keluar dalam hitungan detik.</p>
<a class="cta" href="#coba">Coba prediksi sekarang</a><a class="ghost" href="#cara">Lihat cara kerjanya</a>
</div>
<div>
<div class="dots" role="img" aria-label="{round(rate)} dari 100 kotak berwarna kuning">{dots}</div>
<p class="viz-cap"><b>{round(rate)} dari 100</b> reservasi di data kami akhirnya dibatalkan.</p>
<p class="viz-note">Data Hotel Booking Demand (City Hotel dan Resort Hotel, 2015-2017), setelah baris duplikat dibuang.</p>
</div>
</section>
""")

# ------------------------------------------------------------------ cara kerja
html("""
<div id="cara"></div>
<h2>Cara pakainya</h2>
<div class="steps">
<div class="step"><h4>1. Isi lima info booking</h4><p>Jarak hari sebelum menginap, negara tamu, asal pemesanan, permintaan khusus, dan tipe pelanggan.</p></div>
<div class="step"><h4>2. Model menghitung peluang</h4><p>Model pembelajaran mesin yang sudah dilatih dengan data historis membandingkan booking ini dengan pola yang pernah terjadi.</p></div>
<div class="step"><h4>3. Baca hasilnya</h4><p>Kamu dapat label, persentase peluang batal, dan penjelasan singkat. Hasilnya estimasi, bukan kepastian.</p></div>
</div>
""")

# ------------------------------------------------------------------ prediksi
html('<div id="coba"></div><h2>Coba sendiri</h2>')
st.write("Belum punya data? Pilih salah satu contoh, lalu ubah angkanya sesuka kamu.")
pc = st.columns(len(PRESETS) + 1)
for col, name in zip(pc, PRESETS):
    col.button(name, on_click=apply_preset, args=(name,), key=f"preset_{name}")

left, right = st.columns([1.25, 1], gap="large")
with left:
    with st.container(border=True):
        st.markdown("##### Soal booking-nya")
        a, b = st.columns(2, gap="medium")
        with a:
            lead_time = st.slider("Dipesan berapa hari sebelum menginap?", 0, 365, key="in_lead",
                                  on_change=clear_result)
            st.caption(lead_human(lead_time))
        with b:
            segment = st.selectbox("Dipesan lewat mana?", list(SEGMENT_LABELS), format_func=SEGMENT_LABELS.get,
                                   key="in_segment", on_change=clear_result)
        requests = st.slider("Berapa permintaan khusus dari tamu?", REQ_MIN, REQ_MAX, key="in_requests",
                             on_change=clear_result, help="Contoh: tambahan bed, lantai tinggi, kamar bebas rokok.")
        st.markdown("##### Soal tamunya")
        c, d = st.columns(2, gap="medium")
        with c:
            country = st.selectbox("Tamu berasal dari mana?", country_options, format_func=country_fmt,
                                   key="in_country", on_change=clear_result,
                                   help="Negara di luar daftar dipilih lewat 'Negara lain'.")
        with d:
            customer = st.selectbox("Tipe pelanggan", list(CUSTOMER_LABELS), format_func=CUSTOMER_LABELS.get,
                                    key="in_customer", on_change=clear_result)
        b1, b2 = st.columns([2, 1])
        go = b1.button("Prediksi pembatalan", type="primary", use_container_width=True)
        b2.button("Atur ulang", on_click=reset_form, use_container_width=True)

if go:  # FR-02, FR-03
    inputs = {"lead_time": int(lead_time), "country": country, "market_segment": segment,
              "total_of_special_requests": int(requests), "customer_type": customer}
    errors = validate_inputs(inputs, countries)
    if errors:
        with left:
            for e in errors:
                st.error(e)
        clear_result()
    else:
        proba, label = predict(artifact, inputs)
        st.session_state["result"] = {"proba": proba, "label": label}

with right:  # FR-04, FR-05, FR-06
    res = st.session_state.get("result")
    if not res:
        html("""
        <div class="panel-empty"><b>Hasilnya muncul di sini</b>
        Isi form di sebelah kiri, lalu tekan <i>Prediksi pembatalan</i>. Kamu akan melihat label, peluang batal dalam persen, dan batas yang dipakai model.</div>
        """)
    else:
        p, lab = res["proba"], res["label"]
        pct = f"{p*100:.0f}"
        cls, tag = ("warn", "⚠ Berpotensi dibatalkan") if lab else ("ok", "✓ Tidak berpotensi dibatalkan")
        verdict = "berpotensi dibatalkan" if lab else "tidak berpotensi dibatalkan"
        html(f"""
        <div class="result {cls}">
        <div class="r-tag">{tag}</div>
        <div class="r-num">{pct}<span>%</span></div>
        <div class="r-sub">peluang batal menurut model ({artifact['model_name']})</div>
        <div class="gauge"><div class="fill" style="width:{p*100:.1f}%"></div><div class="tick" style="left:{thr*100:.1f}%"></div></div>
        <div class="g-note">Garis kuning = batas {thr*100:.0f}%. Di atas garis, booking ditandai berpotensi batal. Batas ini sengaja lebih rendah dari 50% supaya model lebih banyak menemukan pembatalan.</div>
        <p class="r-text">Model memperkirakan booking ini <b>{verdict}</b> dengan peluang batal sekitar <b>{pct}%</b>. Ini estimasi dari pola data historis dan tidak menjamin keputusan tamu.</p>
        </div>
        """)

# ------------------------------------------------------------------ keandalan
rec, prec = metrics.get("Recall"), metrics.get("Precision")
if rec and prec:
    html(f"""
    <h2>Seberapa bisa dipercaya?</h2>
    <div class="band">
    <h3>Diuji pada reservasi yang tidak pernah dilihat model saat belajar</h3>
    <div class="grid">
    <div><div class="num">±{rec*100:.0f}</div><p>Dari 100 booking yang memang akhirnya batal, model berhasil menandai sekitar {rec*100:.0f}.</p></div>
    <div><div class="num">±{prec*100:.0f}</div><p>Dari 100 booking yang ditandai berpotensi batal, sekitar {prec*100:.0f} benar-benar batal. Sisanya peringatan keliru.</p></div>
    <div><div class="num">{metrics.get('ROC-AUC', 0):.2f}</div><p>Skor ROC-AUC (maksimum 1,00): ukuran seberapa baik model membedakan booking yang batal dan yang tidak.</p></div>
    </div>
    <p>Yang masih sulit: booking yang dibuat mepet dengan tanggal menginap jauh lebih susah ditebak. Detail lengkap ada di halaman Evaluasi model.</p>
    </div>
    """)

# ------------------------------------------------------------------ tim
html("<h2>Tim di balik proyek</h2>" + team_html())
html('<p class="fine" style="margin-top:2.4rem">Prototipe edukasi untuk proyek akhir Pembelajaran Mesin. Hasil prediksi bukan kepastian dan tidak boleh dipakai sebagai satu-satunya dasar untuk menolak atau memperlakukan pelanggan secara berbeda.</p>')
