"""StayCheck - beranda + prediksi pembatalan booking hotel (Streamlit)."""
from datetime import datetime
from html import escape
import pandas as pd
import plotly.graph_objects as go_plotly
import streamlit as st
from ui import inject_css, top_nav, html, team_html, BRAND, FAVICON
from utils import (require_artifact, known_countries, validate_inputs, predict, cancel_rate_pct,
                   explain_local_drivers, threshold_zone, format_input_value, historical_benchmarks,
                   FIGURES, COUNTRY_NAMES, OTHER_COUNTRY, SEGMENT_LABELS, CUSTOMER_LABELS,
                   LEAD_MIN, LEAD_MAX, REQ_MIN, REQ_MAX)

st.set_page_config(page_title=f"{BRAND} - Prediksi pembatalan booking hotel", page_icon=FAVICON, layout="wide")
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
    "Pesan online jauh hari": {"in_lead": 220, "in_country": "PRT", "in_segment": "Online TA",
                               "in_requests": 0, "in_customer": "Transient"},
    "Tamu perusahaan, mepet": {"in_lead": 3, "in_country": "GBR", "in_segment": "Corporate",
                               "in_requests": 2, "in_customer": "Contract"},
    "Liburan keluarga": {"in_lead": 45, "in_country": "DEU", "in_segment": "Direct",
                         "in_requests": 3, "in_customer": "Transient-Party"},
    "Rombongan tur": {"in_lead": 150, "in_country": "ESP", "in_segment": "Groups",
                      "in_requests": 0, "in_customer": "Group"},
    "Backpacker dadakan": {"in_lead": 1, "in_country": "FRA", "in_segment": "Online TA",
                           "in_requests": 1, "in_customer": "Transient"},
    "Tamu luar Eropa": {"in_lead": 120, "in_country": OTHER_COUNTRY, "in_segment": "Offline TA/TO",
                        "in_requests": 2, "in_customer": "Transient"},
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


def clear_history():
    st.session_state["history"] = []


def lead_human(d):
    if d == 0:
        return "Dipesan di hari yang sama dengan kedatangan."
    if d < 7:
        return f"Dipesan {d} hari sebelum kedatangan (mepet)."
    if d < 30:
        return f"Dipesan sekitar {round(d/7)} minggu sebelum kedatangan."
    if d < 365:
        return f"Dipesan sekitar {round(d/30)} bulan sebelum kedatangan."
    return f"Dipesan lebih dari setahun ({d} hari) sebelum kedatangan; di rentang ekstrem keandalan menurun."


def build_comparison_chart(inputs, proba, threshold, label):
    """Grafik komparasi interaktif (Plotly) antara booking ini dan rata-rata historis."""
    rows = historical_benchmarks(inputs, proba)[::-1]
    categories = [r["Kategori"] for r in rows]
    values = [r["Peluang batal (%)"] for r in rows]
    colors = []
    for r in rows:
        if r["Tipe"] == "Prediksi":
            colors.append("#EF4444" if label else "#10B981")
        elif r["Tipe"] == "Rata-rata":
            colors.append("#64748B")
        else:
            colors.append("#0284C7")

    fig = go_plotly.Figure(
        go_plotly.Bar(
            x=values,
            y=categories,
            orientation="h",
            marker=dict(color=colors, cornerradius=6),
            text=[f"{v:.1f}%" for v in values],
            textposition="outside",
            cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>Rasio/peluang batal: %{x:.1f}%<extra></extra>",
        )
    )
    thr_pct = threshold * 100.0
    fig.add_vline(
        x=thr_pct,
        line_width=2,
        line_dash="dash",
        line_color="#F59E0B",
        annotation_text=f"Batas {thr_pct:.0f}%",
        annotation_position="top right",
        annotation_font=dict(size=11, color="#B45309"),
    )
    fig.update_layout(
        title=dict(
            text="Perbandingan dengan Rata-rata Historis (%)",
            font=dict(family="Bricolage Grotesque, sans-serif", size=15, color="#0F172A"),
            x=0,
        ),
        xaxis=dict(range=[0, max(max(values) + 14, thr_pct + 15, 55)], title=None, showgrid=True, gridcolor="#E2E8F0"),
        yaxis=dict(title=None, tickfont=dict(size=12, color="#0F172A")),
        margin=dict(l=8, r=36, t=38, b=16),
        height=245,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Figtree, sans-serif", color="#0F172A"),
        showlegend=False,
    )
    return fig


# ------------------------------------------------------------------ nav + hero
top_nav()
rate = cancel_rate_pct()
dots = "".join('<i class="on"></i>' if i < round(rate) else "<i></i>" for i in range(100))
html(f"""
<section class="hero">
<div>
<h1>Booking ini bakal batal nggak, ya?</h1>
<p class="lead">{BRAND} membaca pola dari puluhan ribu reservasi hotel untuk memperkirakan peluang sebuah booking dibatalkan. Isi lima info, jawabannya keluar dalam hitungan detik.</p>
<div class="hero-cta"><a class="cta" href="#coba">Coba prediksi sekarang</a><a class="ghost" href="#wawasan">Lihat grafik data</a></div>
</div>
<div class="hero-card">
<div class="hero-photo">
<img src="https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=80" alt="Ilustrasi City & Resort Hotel Portugal" loading="lazy"/>
<span class="badge">Dataset Portugal 2015–2017 · 87.151 reservasi unik</span>
</div>
<div class="dots" role="img" aria-label="{round(rate)} dari 100 kotak berwarna biru">{dots}</div>
<p class="viz-cap"><b>{round(rate)} dari 100</b> reservasi di data kami akhirnya dibatalkan.</p>
<p class="viz-note">Data Hotel Booking Demand (City Hotel Lisbon & Resort Hotel Algarve), setelah baris duplikat dibuang.</p>
</div>
</section>
""")

# ------------------------------------------------------------------ cara kerja
html("""
<div id="cara"></div>
<h2>Cara pakainya</h2>
<div class="steps">
<div class="step">
<div class="step-head"><span class="step-badge">01</span><span class="step-tag">Input 5 Fitur</span></div>
<h4>Masukkan profil reservasi</h4>
<p>Atur jarak hari sebelum check-in, negara asal tamu, kanal pemesanan, jumlah permintaan khusus, dan tipe pelanggan.</p>
</div>
<div class="step">
<div class="step-head"><span class="step-badge">02</span><span class="step-tag">Skor Risiko</span></div>
<h4>Pipeline menghitung peluang</h4>
<p>Model membandingkan profil ini terhadap 87.151 histori reservasi City & Resort Hotel Portugal secara instan.</p>
</div>
<div class="step">
<div class="step-head"><span class="step-badge">03</span><span class="step-tag">Keputusan</span></div>
<h4>Analisis faktor pendorong</h4>
<p>Lihat persentase risiko batal, posisinya terhadap ambang batas, serta 3 faktor utama yang mendorong skor tersebut.</p>
</div>
</div>
""")

# ------------------------------------------------------------------ prediksi
html('<div id="coba"></div><h2>Coba sendiri</h2>')
st.write("Belum punya data? Klik salah satu skenario cepat di bawah ini, lalu sesuaikan angkanya:")
with st.container(key="preset_bar"):
    pc = st.columns(len(PRESETS), gap="small")
    for col, name in zip(pc, PRESETS):
        col.button(name, on_click=apply_preset, args=(name,), key=f"preset_{name}")

left, right = st.columns([1.25, 1], gap="large")
with left:
    with st.container(border=True):
        st.markdown("##### Soal booking-nya")
        a, b = st.columns(2, gap="medium")
        with a:
            lead_time = st.slider("Dipesan berapa hari sebelum menginap?", LEAD_MIN, 365, key="in_lead",
                                  on_change=clear_result,
                                  help=f"Rentang umum 0-365 hari (maksimum data latih: {LEAD_MAX} hari).")
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
                                   help=f"{len(countries)} negara teratas punya kategori sendiri; negara di luar daftar dipetakan ke 'Negara lain' oleh pipeline.")
        with d:
            customer = st.selectbox("Tipe pelanggan", list(CUSTOMER_LABELS), format_func=CUSTOMER_LABELS.get,
                                    key="in_customer", on_change=clear_result)
        b1, b2 = st.columns([2, 1])
        go = b1.button("Prediksi pembatalan", type="primary", width="stretch")
        b2.button("Atur ulang", on_click=reset_form, width="stretch")

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
        drivers = explain_local_drivers(artifact, inputs)
        st.session_state["result"] = {"proba": proba, "label": label, "inputs": inputs, "drivers": drivers}
        hist = st.session_state.setdefault("history", [])
        hist.insert(0, {
            "Waktu": datetime.now().strftime("%H:%M:%S"),
            "Jarak (hari)": int(lead_time),
            "Negara": country_fmt(country),
            "Asal pemesanan": SEGMENT_LABELS.get(segment, segment),
            "Permintaan khusus": int(requests),
            "Tipe pelanggan": CUSTOMER_LABELS.get(customer, customer),
            "Peluang batal (%)": round(proba * 100, 1),
            "Status": "Berpotensi batal" if label else "Tidak berpotensi batal",
        })
        del hist[10:]

with right:  # FR-04, FR-05, FR-06
    res = st.session_state.get("result")
    if not res:
        html("""
        <div class="panel-empty"><b>Hasilnya muncul di sini</b>
        Isi form di sebelah kiri, lalu tekan <i>Prediksi pembatalan</i>. Kamu akan melihat label, peluang batal dalam persen, batas yang dipakai model, dan faktor pendorong utamanya.</div>
        """)
    else:
        p, lab = res["proba"], res["label"]
        pct = f"{p*100:.0f}"
        cls, tag = ("warn", "⚠ Berpotensi dibatalkan") if lab else ("ok", "✓ Tidak berpotensi dibatalkan")
        verdict = "berpotensi dibatalkan" if lab else "tidak berpotensi dibatalkan"
        z_code, z_text = threshold_zone(p, thr)
        z_cls = "near" if z_code == "near" else ""
        drivers = res.get("drivers") or explain_local_drivers(artifact, res.get("inputs", {
            "lead_time": int(lead_time), "country": country, "market_segment": segment,
            "total_of_special_requests": int(requests), "customer_type": customer,
        }))
        driver_items = []
        for d_row in drivers[:3]:
            dp = d_row["delta_pp"]
            if dp > 0.5:
                badge = f'<span class="d-up">↑ +{dp:.1f} poin risiko</span>'
            elif dp < -0.5:
                badge = f'<span class="d-down">↓ {dp:.1f} poin risiko</span>'
            else:
                badge = '<span class="d-flat">≈ netral vs profil acuan</span>'
            driver_items.append(
                f'<li><span><b>{escape(d_row["title"])}:</b> {escape(d_row["value"])}</span>{badge}</li>'
            )
        drivers_block = (
            f'<div class="r-drivers"><h4>Mengapa hasilnya seperti ini?</h4>'
            f'<ul>{"".join(driver_items)}</ul></div>'
        )
        html(f"""
        <div class="result {cls}">
        <div class="r-tag">{tag}</div>
        <div class="r-num">{pct}<span>%</span></div>
        <div class="r-sub">peluang batal menurut model ({artifact['model_name']})</div>
        <div class="r-zone {z_cls}">{escape(z_text)}</div>
        <div class="gauge"><div class="fill" style="width:{p*100:.1f}%"></div><div class="tick" style="left:{thr*100:.1f}%"></div></div>
        <div class="g-note">Garis kuning = batas {thr*100:.0f}%. Di atas garis, booking ditandai berpotensi batal. Batas ini sengaja lebih rendah dari 50% supaya model lebih banyak menemukan pembatalan.</div>
        <p class="r-text">Model memperkirakan booking ini <b>{verdict}</b> dengan peluang batal sekitar <b>{pct}%</b>. Ini estimasi dari pola data historis dan tidak menjamin keputusan tamu.</p>
        {drivers_block}
        </div>
        """)
        curr_inputs = res.get("inputs", {
            "lead_time": int(lead_time), "country": country, "market_segment": segment,
            "total_of_special_requests": int(requests), "customer_type": customer,
        })
        with st.container(border=True):
            st.plotly_chart(
                build_comparison_chart(curr_inputs, p, thr, lab),
                width="stretch",
                config={"displayModeBar": False},
            )

# ------------------------------------------------------------------ riwayat & ekspor sesi
hist_rows = st.session_state.get("history", [])
if hist_rows:
    with st.expander(f"Riwayat prediksi sesi ini ({len(hist_rows)} percobaan)", expanded=False):
        hist_df = pd.DataFrame(hist_rows)
        st.dataframe(hist_df, width="stretch", hide_index=True)
        hc1, hc2 = st.columns([1, 1])
        hc1.download_button(
            "Unduh riwayat (CSV)",
            data=hist_df.to_csv(index=False).encode("utf-8"),
            file_name="riwayat_prediksi_staycheck.csv",
            mime="text/csv",
            width="stretch",
        )
        hc2.button("Hapus riwayat", on_click=clear_history, width="stretch")

# ------------------------------------------------------------------ wawasan visual EDA
html('<div id="wawasan"></div><h2>Wawasan visual dari data historis</h2>')
st.write("Grafik eksplorasi dari 87.151 reservasi unik yang menjelaskan pola pembatalan sebelum model dilatih.")
eda_t1, eda_t2, eda_t3, eda_t4 = st.tabs([
    "Jarak Pesan, Bulan & Negara",
    "Segmen & Tipe Tamu",
    "Permintaan Khusus",
    "Proporsi Target",
])
with eda_t1:
    p_lt = FIGURES / "leadtime_month_country.png"
    if p_lt.exists():
        st.image(str(p_lt), width="stretch")
    st.caption("Semakin jauh hari pemesanan (lead time), semakin tinggi rasio batal: dari 8,4% (0–7 hari) naik hingga 39,3% (181–365 hari). Sepuluh negara teratas mencakup ≈82% dari total reservasi.")
with eda_t2:
    p_cat = FIGURES / "cat_cancel_rate.png"
    if p_cat.exists():
        st.image(str(p_cat), width="stretch")
    st.caption("Pemesanan melalui Online TA memiliki rasio batal tertinggi (35,2%) dibanding Direct (14,7%) dan Corporate (11,9%). Tamu perorangan (Transient) juga lebih sering batal (30,0%) dibanding kontrak/grup.")
with eda_t3:
    p_req = FIGURES / "requests_parking.png"
    if p_req.exists():
        st.image(str(p_req), width="stretch")
    st.caption("Tamu dengan permintaan khusus cenderung lebih berkomitmen datang (0 permintaan: 32,9% batal vs 3 permintaan: 17,1% batal). Slot parkir tidak dipakai sebagai fitur karena terindikasi data leakage.")
with eda_t4:
    p_tgt = FIGURES / "target_dist.png"
    if p_tgt.exists():
        st.image(str(p_tgt), width="stretch")
    st.caption("Distribusi kelas setelah pembersihan duplikat: sekitar 27,3% reservasi dibatalkan dan 72,7% tidak dibatalkan.")

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
