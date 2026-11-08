"""Tentang proyek."""
import streamlit as st
from ui import inject_css, top_nav, html, team_html, BRAND, FAVICON
from utils import FIGURES

st.set_page_config(page_title=f"{BRAND} - Tentang proyek", page_icon=FAVICON, layout="wide")
inject_css()
top_nav()

html("""<section class="hero" style="grid-template-columns:1fr;padding-bottom:0"><div>
<h1 style="font-size:2.8rem">Cerita di balik proyek ini</h1>
<p class="lead">Pembatalan booking bikin kamar kosong mendadak dan pendapatan hotel meleset. Kami mencoba menjawabnya dengan data.</p></div></section>""")

html("""
<div class="photo-grid">
<div class="photo-card">
<img src="https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=900&q=80" alt="City Hotel Lisbon Portugal" loading="lazy"/>
<div class="pc-body">
<span class="pc-tag">City Hotel · Lisbon, Portugal (Rasio batal 29,8%)</span>
<h4>Hotel Perkotaan & Perjalanan Bisnis</h4>
<p>Mayoritas reservasi dipesan lewat agen travel online (Online TA) dengan perputaran tamu cepat dan risiko pembatalan lebih tinggi.</p>
</div>
</div>
<div class="photo-card">
<img src="https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=900&q=80" alt="Resort Hotel Algarve Portugal" loading="lazy"/>
<div class="pc-body">
<span class="pc-tag">Resort Hotel · Algarve, Portugal (Rasio batal 23,3%)</span>
<h4>Hotel Resor & Liburan Musiman</h4>
<p>Dominan tamu liburan dengan durasi menginap lebih panjang dan puncak kedatangan pada musim panas Eropa (Juli–Agustus).</p>
</div>
</div>
</div>
""")

c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown("## Masalahnya")
    st.write("Pembatalan reservasi memengaruhi perencanaan kamar, pendapatan, dan operasional hotel. "
             "Proyek ini membangun model klasifikasi untuk memperkirakan apakah suatu reservasi berpotensi "
             "dibatalkan, sebagai proyek akhir mata kuliah Pembelajaran Mesin.")
    st.markdown("## Datanya")
    st.write("**Hotel Booking Demand**: catatan reservasi City Hotel dan Resort Hotel periode 2015-2017, "
             "sekitar 119 ribu baris. Setelah baris duplikat dibuang tersisa sekitar 87 ribu baris.")
    st.markdown("- Kaggle: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand\n"
                "- Publikasi: Antonio, de Almeida & Nunes (2019), *Data in Brief* 22, 41-49. "
                "https://doi.org/10.1016/j.dib.2018.11.126")
with c2:
    st.markdown("## Yang kami bangun")
    st.write("Model memakai lima input: jarak pemesanan ke kedatangan, negara asal tamu, asal pemesanan, "
             "jumlah permintaan khusus, dan tipe pelanggan. Tiga algoritma dibandingkan: **Logistic Regression**, "
             "**Random Forest**, dan **XGBoost**. Model dilatih pada data latih, di-tuning dengan cross-validation, "
             "lalu diuji sekali pada data uji.")
    st.caption(
        "Catatan pra-pemrosesan: negara di luar 10 negara terbanyak digabung ke kategori `OTHER` oleh pipeline; "
        "baris `market_segment = Undefined` (2 baris pada data mentah) tidak disediakan sebagai pilihan input "
        "dan ditangani otomatis oleh encoder dengan `handle_unknown='ignore'`."
    )
    st.markdown("## Keterbatasan")
    st.markdown(
        "- Data historis 2015-2017 dari konteks hotel tertentu; pola belum tentu berlaku di hotel, negara, atau periode lain.\n"
        "- Model mempelajari pola statistik, **bukan alasan pasti** seseorang membatalkan booking.\n"
        "- Booking yang dibuat mepet dengan tanggal menginap sulit dideteksi.\n"
        "- Persentase adalah estimasi; sebagian booking yang tidak batal ikut ditandai.\n"
        "- Hasil tidak boleh jadi satu-satunya dasar untuk menolak atau memperlakukan pelanggan secara berbeda.\n"
        "- Negara asal tamu dipakai karena berkorelasi dengan pola pembatalan di data, bukan karena negara menyebabkan pembatalan; jangan dipakai untuk membedakan perlakuan tamu.\n"
        "- Data dibagi acak, bukan berdasarkan waktu, sehingga performa pada periode yang lebih baru belum teruji.\n"
        "- Prototipe edukasi, bukan sistem operasional hotel.")

st.markdown("## Karakteristik Statistik Data")
da1, da2 = st.tabs(["Distribusi Fitur Numerik", "Korelasi Antar Fitur"])
with da1:
    p_num = FIGURES / "numeric_dist.png"
    if p_num.exists():
        st.image(str(p_num), width="stretch")
    st.caption("Distribusi jarak pemesanan (lead_time), lama menginap, jumlah tamu, dan tarif harian rata-rata (ADR) yang cenderung miring ke kanan (right-skewed).")
with da2:
    p_cor = FIGURES / "corr_heatmap.png"
    if p_cor.exists():
        st.image(str(p_cor), width="stretch")
    st.caption("Korelasi linear Pearson antar fitur numerik. Hubungan non-linear dan fitur kategorikal ditangkap lebih baik oleh model berbasis pohon (Random Forest & XGBoost).")

html("<h2>Tim</h2>" + team_html())
