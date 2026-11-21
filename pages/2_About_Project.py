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
<div class="hero-carousel" style="height:200px;margin:0;border-radius:0" role="img" aria-label="Carousel City Hotel Lisbon">
<div class="c-slide"><img src="https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?auto=format&fit=crop&w=900&q=80" alt="City Hotel Lisbon 1" loading="lazy"/><div class="c-cap">Fasad &amp; Kamar Urban<small>Lisbon, Portugal</small></div></div>
<div class="c-slide"><img src="https://images.unsplash.com/photo-1566665797739-1674de7a421a?auto=format&fit=crop&w=900&q=80" alt="City Hotel Lisbon 2" loading="lazy"/><div class="c-cap">Interior Kamar Bisnis<small>Dominan tamu Online TA</small></div></div>
<div class="c-slide"><img src="https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=900&q=80" alt="City Hotel Lisbon 3" loading="lazy"/><div class="c-cap">Arus Kedatangan Harian<small>Perputaran reservasi tinggi</small></div></div>
<div class="c-slide"><img src="https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=900&q=80" alt="City Hotel Lisbon 4" loading="lazy"/><div class="c-cap">Suite Eksekutif<small>Tamu perjalanan singkat</small></div></div>
<div class="c-dots"><i></i><i></i><i></i><i></i></div>
</div>
<div class="pc-body">
<span class="pc-tag">City Hotel · Lisbon, Portugal (Rasio batal 29,8%)</span>
<h4>Hotel Perkotaan &amp; Perjalanan Bisnis</h4>
<p>Mayoritas reservasi dipesan lewat agen travel online (Online TA) dengan perputaran tamu cepat dan risiko pembatalan lebih tinggi.</p>
</div>
</div>
<div class="photo-card">
<div class="hero-carousel" style="height:200px;margin:0;border-radius:0" role="img" aria-label="Carousel Resort Hotel Algarve">
<div class="c-slide"><img src="https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=900&q=80" alt="Resort Hotel Algarve 1" loading="lazy"/><div class="c-cap">Pemandangan Pantai Algarve<small>Selatan Portugal</small></div></div>
<div class="c-slide"><img src="https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=900&q=80" alt="Resort Hotel Algarve 2" loading="lazy"/><div class="c-cap">Kolam Renang Resor<small>Puncak tamu Juli–Agustus</small></div></div>
<div class="c-slide"><img src="https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=900&q=80" alt="Resort Hotel Algarve 3" loading="lazy"/><div class="c-cap">Vila &amp; Area Bersantai<small>Durasi menginap lebih panjang</small></div></div>
<div class="c-slide"><img src="https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?auto=format&fit=crop&w=900&q=80" alt="Resort Hotel Algarve 4" loading="lazy"/><div class="c-cap">Balkon Menghadap Laut<small>Dominan liburan keluarga</small></div></div>
<div class="c-dots"><i></i><i></i><i></i><i></i></div>
</div>
<div class="pc-body">
<span class="pc-tag">Resort Hotel · Algarve, Portugal (Rasio batal 23,3%)</span>
<h4>Hotel Resor &amp; Liburan Musiman</h4>
<p>Dominan tamu liburan dengan durasi menginap lebih panjang dan puncak kedatangan pada musim panas Eropa (Juli–Agustus).</p>
</div>
</div>
</div>
""")

html("""
<div class="about-grid">
<div class="about-card">
<span class="a-tag">Masalah</span>
<h3>Masalahnya</h3>
<p>Pembatalan reservasi memengaruhi perencanaan kamar, pendapatan, dan operasional hotel. Proyek ini membangun model klasifikasi untuk memperkirakan apakah suatu reservasi berpotensi dibatalkan, sebagai proyek akhir mata kuliah Pembelajaran Mesin.</p>
</div>
<div class="about-card">
<span class="a-tag">Data</span>
<h3>Datanya</h3>
<p><b>Hotel Booking Demand</b>: reservasi City Hotel dan Resort Hotel periode 2015-2017.</p>
<div class="a-chips"><span>±119 ribu baris mentah</span><span>±87 ribu setelah duplikat dibuang</span><span>2015-2017</span></div>
<ul>
<li><a href="https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand" target="_blank">Kaggle: Hotel Booking Demand</a></li>
<li>Antonio, de Almeida &amp; Nunes (2019), <i>Data in Brief</i> 22, 41-49. <a href="https://doi.org/10.1016/j.dib.2018.11.126" target="_blank">doi.org/10.1016/j.dib.2018.11.126</a></li>
</ul>
</div>
<div class="about-card">
<span class="a-tag">Model</span>
<h3>Yang kami bangun</h3>
<p>Model memakai <b>10 input</b>, dibandingkan pada tiga algoritma, dilatih di data latih, di-tuning dengan cross-validation, lalu diuji sekali pada data uji.</p>
<div class="a-chips"><span>Jarak pemesanan</span><span>Negara tamu</span><span>Asal pemesanan</span><span>Permintaan khusus</span><span>Tipe pelanggan</span><span>Jenis hotel</span><span>Lama menginap</span><span>Tarif per malam</span><span>Pembatalan sebelumnya</span><span>Status tamu berulang</span></div>
<div class="a-chips algo"><span>Logistic Regression</span><span>Random Forest</span><span>XGBoost</span></div>
<p class="a-note">Negara di luar 10 negara terbanyak digabung ke kategori <code>OTHER</code> oleh pipeline. Baris <code>market_segment = Undefined</code> (2 baris) tidak disediakan sebagai pilihan input dan ditangani encoder dengan <code>handle_unknown='ignore'</code>.</p>
</div>
<div class="about-card warn">
<span class="a-tag">Perhatian</span>
<h3>Keterbatasan</h3>
<ul>
<li>Data historis 2015-2017 dari hotel tertentu; belum tentu berlaku di hotel, negara, atau periode lain.</li>
<li>Model mempelajari pola statistik, <b>bukan alasan pasti</b> seseorang membatalkan booking.</li>
<li>Booking yang dibuat mepet dengan tanggal menginap sulit dideteksi.</li>
<li>Persentase adalah estimasi; sebagian booking yang tidak batal ikut ditandai.</li>
<li>Hasil tidak boleh jadi satu-satunya dasar untuk menolak atau memperlakukan pelanggan secara berbeda.</li>
<li>Negara asal, riwayat pembatalan, dan status tamu berulang hanya pola statistik; jangan dipakai membedakan perlakuan tamu.</li>
<li>Tarif per malam dalam euro, tingkat harga Portugal 2015-2017; tidak setara harga hotel di Indonesia.</li>
<li>Data dibagi acak, bukan berdasarkan waktu, sehingga performa pada periode lebih baru belum teruji.</li>
<li>Prototipe edukasi, bukan sistem operasional hotel.</li>
</ul>
</div>
</div>
""")

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