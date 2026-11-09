"""StayCheck - beranda + prediksi pembatalan booking hotel (Streamlit)."""
from datetime import datetime
from html import escape
import pandas as pd
import plotly.graph_objects as go_plotly
import streamlit as st
from ui import inject_css, top_nav, html, team_html, BRAND, FAVICON
import importlib
import utils as _utils
if not hasattr(_utils, "operational_recommendations"):
    _utils = importlib.reload(_utils)
from utils import (require_artifact, known_countries, validate_inputs, predict, cancel_rate_pct,
                   explain_local_drivers, threshold_zone, format_input_value, historical_benchmarks,
                   operational_recommendations, what_if_scenarios, sample_batch_dataframe, predict_batch,
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
            "in_segment": "Online TA", "in_requests": 0, "in_customer": "Transient",
            "in_adr": 750_000, "in_nights": 2}
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
            font=dict(family="Bricolage Grotesque, sans-serif", size=14, color="#0F172A"),
            x=0,
        ),
        xaxis=dict(range=[0, max(max(values) + 14, thr_pct + 15, 55)], title=None, showgrid=True, gridcolor="#E2E8F0"),
        yaxis=dict(title=None, tickfont=dict(size=11.5, color="#0F172A"), automargin=True),
        margin=dict(l=4, r=32, t=30, b=10),
        height=205,
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
<div class="hero-kicker">Model {artifact['model_name']} · Proyek Akhir Pembelajaran Mesin 2026</div>
<h1>Booking ini bakal batal nggak, ya?</h1>
<p class="lead">{BRAND} membaca pola dari puluhan ribu reservasi hotel untuk memperkirakan peluang sebuah booking dibatalkan. Isi lima info, jawabannya keluar dalam hitungan detik.</p>
<div class="hero-cta"><a class="cta" href="#coba">Coba prediksi sekarang</a><a class="ghost" href="#wawasan">Lihat grafik data</a></div>
<div class="hero-stats">
<div class="h-stat"><b>87.151</b><span>reservasi unik dipelajari</span></div>
<div class="h-stat"><b>{metrics.get('ROC-AUC', 0):.2f}</b><span>ROC-AUC pada data uji</span></div>
<div class="h-stat"><b>{thr*100:.0f}%</b><span>batas penandaan risiko</span></div>
</div>
</div>
<div class="hero-card">
<div class="hero-carousel" role="img" aria-label="Galeri foto suasana hotel yang berganti otomatis">
<div class="c-slide"><img src="https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=80" alt="Resort hotel dengan kolam renang" loading="lazy"/><div class="c-cap">Resort Hotel · Algarve<small>Liburan musiman, rasio batal 23,3%</small></div></div>
<div class="c-slide"><img src="https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=900&q=80" alt="City hotel modern" loading="lazy"/><div class="c-cap">City Hotel · Lisbon<small>Tamu bisnis &amp; online, rasio batal 29,8%</small></div></div>
<div class="c-slide"><img src="https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=900&q=80" alt="Suasana kamar dan balkon resor" loading="lazy"/><div class="c-cap">Pola Musiman · Puncak Juli–Agustus<small>Lead time panjang cenderung lebih rawan batal</small></div></div>
<div class="c-slide"><img src="https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=900&q=80" alt="Area kedatangan tamu hotel" loading="lazy"/><div class="c-cap">Rekam Historis · 2015–2017<small>87.151 reservasi dari lebih dari 100 negara asal tamu</small></div></div>
<div class="c-dots"><i></i><i></i><i></i><i></i></div>
</div>
<div class="dots" role="img" aria-label="{round(rate)} dari 100 kotak berwarna biru">{dots}</div>
<p class="viz-cap"><b>{round(rate)} dari 100</b> reservasi di data kami akhirnya dibatalkan.</p>
<p class="viz-note">Data Hotel Booking Demand (City Hotel Lisbon &amp; Resort Hotel Algarve), setelah baris duplikat dibuang.</p>
</div>
</section>
""")

# ------------------------------------------------------------------ cara kerja
html("""
<div id="cara"></div>
<h2>Cara pakainya</h2>
<div class="how-wrap">
<div class="how-side">
<div>
<span class="hs-kicker">Alur 3 langkah</span>
<h3>Dari data booking ke skor risiko dalam hitungan detik</h3>
<p>Tidak perlu paham machine learning. Cukup isi profil reservasi, model yang sudah dilatih akan membandingkannya dengan pola historis.</p>
</div>
<div class="hs-chips"><span>Jarak pemesanan</span><span>Negara</span><span>Kanal pesan</span><span>Permintaan khusus</span><span>Tipe tamu</span></div>
</div>
<div class="how-list">
<div class="how-row"><div class="how-num">01</div><div class="how-body"><h4>Masukkan profil reservasi</h4><p>Atur lima isian di form, atau klik salah satu skenario cepat.</p></div><span class="how-pill">± 30 detik</span></div>
<div class="how-row"><div class="how-num">02</div><div class="how-body"><h4>Model menghitung peluang batal</h4><p>Pipeline memproses input dan membandingkannya dengan 87 ribu histori reservasi.</p></div><span class="how-pill">Instan</span></div>
<div class="how-row"><div class="how-num">03</div><div class="how-body"><h4>Baca hasil &amp; faktor pendorong</h4><p>Lihat persentase, posisi terhadap batas, grafik pembanding, dan 3 faktor utama.</p></div><span class="how-pill">Estimasi</span></div>
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
    with st.container(key="form_box"):
        html('<div class="form-banner"><b>Form prediksi pembatalan</b><span>5 input</span></div>')
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
        curr_inputs = res.get("inputs", {
            "lead_time": int(lead_time), "country": country, "market_segment": segment,
            "total_of_special_requests": int(requests), "customer_type": customer,
        })
        stamp_info, actions = operational_recommendations(p, thr, curr_inputs)
        stamp_text, stamp_cls = stamp_info
        actions_html = "".join(f"<li>{escape(act)}</li>" for act in actions)
        html(f"""
        <div class="result {cls}">
        <div class="r-head"><div class="r-tag">{tag}</div><span class="r-stamp {stamp_cls}">{escape(stamp_text)}</span></div>
        <div class="r-score-row">
        <div><div class="r-num">{pct}<span>%</span></div><div class="r-sub">peluang batal menurut model ({artifact['model_name']})</div></div>
        <div class="r-zone {z_cls}">{escape(z_text)}</div>
        </div>
        <div class="gauge"><div class="fill" style="width:{p*100:.1f}%"></div><div class="tick" style="left:{thr*100:.1f}%"></div></div>
        <div class="g-note">Garis kuning = batas {thr*100:.0f}%. Booking ini diperkirakan <b>{verdict}</b> (~{pct}% peluang batal berdasarkan pola historis).</div>
        {drivers_block}
        <div class="r-actions"><h4>Rekomendasi langkah operasional hotel</h4><ol>{actions_html}</ol></div>
        </div>
        """)
        with st.container(border=True):
            st.plotly_chart(
                build_comparison_chart(curr_inputs, p, thr, lab),
                width="stretch",
                config={"displayModeBar": False},
            )

# ------------------------------------------------------------------ simulasi bisnis & what-if (Muncul bila sudah ada hasil)
res_active = st.session_state.get("result")
if res_active:
    p_act = res_active["proba"]
    inp_act = res_active["inputs"]
    st.markdown("### Simulasi lanjutan untuk booking ini")
    sim_t1, sim_t2 = st.tabs([
        "Kalkulator Dampak Finansial Kamar",
        "Simulator Sensitivitas 'Bagaimana Jika...'",
    ])
    with sim_t1:
        fc_in, fc_out = st.columns([1, 2.25], gap="medium")
        with fc_in:
            adr_rp = st.number_input("Tarif kamar / malam (Rp)", min_value=100_000, max_value=25_000_000, step=50_000, key="in_adr")
            nights = st.number_input("Durasi menginap (malam)", min_value=1, max_value=30, step=1, key="in_nights")
        gross_val = int(adr_rp) * int(nights)
        exp_loss = int(round(gross_val * p_act))
        rec_deposit = int(round(gross_val * (0.5 if p_act >= thr else 0.25)))
        fmt_rp = lambda n: f"Rp {n:,.0f}".replace(",", ".")
        with fc_out:
            html(f"""
            <div class="fin-grid" style="margin-top:.15rem">
            <div class="fin-card"><small>Total Nilai Reservasi</small><b>{fmt_rp(gross_val)}</b><span>{int(nights)} malam × {fmt_rp(int(adr_rp))}</span></div>
            <div class="fin-card"><small>Ekspektasi Risiko</small><b>{fmt_rp(exp_loss)}</b><span>Nilai × {p_act*100:.1f}% peluang batal</span></div>
            <div class="fin-card"><small>Saran Deposit</small><b>{fmt_rp(rec_deposit)}</b><span>{"50% (risiko di atas batas)" if p_act >= thr else "25% (komitmen standar)"}</span></div>
            </div>
            """)
            st.caption("Ekspektasi risiko finansial menunjukkan potensi pendapatan kamar yang berisiko hilang bila booking batal tanpa pengganti.")
    with sim_t2:
        st.caption("Perubahan skor prediksi jika satu karakteristik dari booking ini berubah:")
        wi_rows = what_if_scenarios(artifact, inp_act)
        wi_cards = []
        for w in wi_rows:
            d_val = w["Perubahan (poin %)"]
            if d_val < -0.5:
                b_cls, b_txt = "wi-down", f"↓ {d_val:.1f}% (jadi {w['Peluang Baru (%)']:.0f}%)"
            elif d_val > 0.5:
                b_cls, b_txt = "wi-up", f"↑ +{d_val:.1f}% (jadi {w['Peluang Baru (%)']:.0f}%)"
            else:
                b_cls, b_txt = "wi-flat", f"Tetap {w['Peluang Baru (%)']:.0f}%"
            wi_cards.append(
                f'<div class="whatif-item"><div><b>{escape(w["Skenario"])}</b>'
                f'<small>Peluang batal awal: {p_act*100:.0f}%</small></div>'
                f'<span class="wi-badge {b_cls}">{b_txt}</span></div>'
            )
        html(f'<div class="whatif-grid">{"".join(wi_cards)}</div>')

# ------------------------------------------------------------------ prediksi daftar booking (Batch CSV)
with st.expander("Prediksi banyak reservasi sekaligus (Simulasi daftar / Upload CSV)", expanded=False):
    b_top1, b_top2 = st.columns([1.45, 1], gap="medium")
    sample_df = sample_batch_dataframe()
    with b_top1:
        st.caption("Unggah CSV dengan 5 kolom (`lead_time`, `country`, `market_segment`, `total_of_special_requests`, `customer_type`) atau uji langsung dengan sampel:")
        btn_c1, btn_c2 = st.columns(2, gap="small")
        btn_c1.download_button(
            "Unduh template CSV",
            data=sample_df.to_csv(index=False).encode("utf-8"),
            file_name="contoh_daftar_booking.csv",
            mime="text/csv",
            width="stretch",
        )
        use_sample = btn_c2.button("Jalankan 8 sampel", width="stretch")
    with b_top2:
        uploaded_csv = st.file_uploader("Unggah CSV daftar booking", type=["csv"], label_visibility="collapsed")
    batch_source = None
    if uploaded_csv is not None:
        try:
            batch_source = pd.read_csv(uploaded_csv)
        except Exception as exc:
            st.error(f"File CSV tidak dapat dibaca: {exc}")
    elif use_sample or st.session_state.get("batch_demo_active"):
        st.session_state["batch_demo_active"] = True
        batch_source = sample_df

    if batch_source is not None:
        try:
            batch_out = predict_batch(artifact, batch_source, countries)
            n_total = len(batch_out)
            n_risk = int((batch_out["Status Prediksi"] == "Berpotensi batal").sum())
            avg_prob = float(batch_out["Peluang Batal (%)"].mean())
            bm1, bm2, bm3 = st.columns(3)
            bm1.metric("Total reservasi diproses", f"{n_total} baris")
            bm2.metric("Ditandai berpotensi batal", f"{n_risk} dari {n_total}")
            bm3.metric("Rata-rata peluang batal", f"{avg_prob:.1f}%")
            st.dataframe(batch_out, width="stretch", hide_index=True)
        except Exception as exc:
            st.error(str(exc))

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
    <div><div class="num">{metrics.get('ROC-AUC', 0):.3f}</div><p>Skor ROC-AUC (maksimum 1,00): ukuran seberapa baik model membedakan booking yang batal dan yang tidak.</p></div>
    </div>
    <p>Yang masih sulit: booking yang dibuat mepet dengan tanggal menginap jauh lebih susah ditebak. Detail lengkap ada di halaman Evaluasi model.</p>
    </div>
    """)

# ------------------------------------------------------------------ tim
html("<h2>Tim di balik proyek</h2>" + team_html())
html('<p class="fine" style="margin-top:2.4rem">Prototipe edukasi untuk proyek akhir Pembelajaran Mesin. Hasil prediksi bukan kepastian dan tidak boleh dipakai sebagai satu-satunya dasar untuk menolak atau memperlakukan pelanggan secara berbeda. Negara asal tamu dipakai hanya karena berkorelasi dengan pola pembatalan di data historis, bukan sebagai dasar membedakan tamu.</p>')
