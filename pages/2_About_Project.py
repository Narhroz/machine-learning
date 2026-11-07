"""Tentang proyek."""
import streamlit as st
from ui import inject_css, top_nav, html, team_html, BRAND

st.set_page_config(page_title=f"{BRAND} - Tentang proyek", page_icon="ℹ️", layout="wide")
inject_css()
top_nav()

html("""<section class="hero" style="grid-template-columns:1fr;padding-bottom:0"><div>
<h1 style="font-size:2.8rem">Cerita di balik proyek ini</h1>
<p class="lead">Pembatalan booking bikin kamar kosong mendadak dan pendapatan hotel meleset. Kami mencoba menjawabnya dengan data.</p></div></section>""")

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
    st.markdown("## Keterbatasan")
    st.markdown(
        "- Data historis 2015-2017 dari konteks hotel tertentu; pola belum tentu berlaku di hotel, negara, atau periode lain.\n"
        "- Model mempelajari pola statistik, **bukan alasan pasti** seseorang membatalkan booking.\n"
        "- Booking yang dibuat mepet dengan tanggal menginap sulit dideteksi.\n"
        "- Persentase adalah estimasi; sebagian booking yang tidak batal ikut ditandai.\n"
        "- Hasil tidak boleh jadi satu-satunya dasar untuk menolak atau memperlakukan pelanggan secara berbeda.\n"
        "- Prototipe edukasi, bukan sistem operasional hotel.")

html("<h2>Tim</h2>" + team_html())
