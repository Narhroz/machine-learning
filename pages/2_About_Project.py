"""Halaman tentang proyek."""
import streamlit as st
from utils import SEGMENT_LABELS

st.set_page_config(page_title="About Project", page_icon="ℹ️", layout="centered")
st.title("ℹ️ Tentang Proyek")

st.subheader("Latar belakang")
st.write("Pembatalan reservasi memengaruhi perencanaan kamar, pendapatan, dan operasional hotel. "
         "Proyek ini membangun model klasifikasi (Machine Learning) untuk memperkirakan apakah suatu "
         "reservasi hotel berpotensi dibatalkan, sebagai proyek akhir mata kuliah Pembelajaran Mesin.")

st.subheader("Dataset")
st.write("**Hotel Booking Demand** (City Hotel dan Resort Hotel, periode 2015-2017, sekitar 119 ribu catatan "
         "reservasi). Setelah baris duplikat dihapus tersisa sekitar 87 ribu baris.")
st.markdown("- Kaggle: https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand  \n"
            "- Publikasi: Antonio, de Almeida & Nunes (2019), *Data in Brief* 22, 41-49. "
            "https://doi.org/10.1016/j.dib.2018.11.126")

st.subheader("Input dan algoritma")
st.write("Model memakai lima input: jarak pemesanan ke kedatangan, negara asal tamu, asal pemesanan, "
         "jumlah permintaan khusus, dan tipe pelanggan. Tiga algoritma dibandingkan: **Logistic Regression**, "
         "**Random Forest**, dan **XGBoost**. Model dilatih pada data latih, di-tuning dengan cross-validation, "
         "dan diuji sekali pada data uji.")

st.subheader("Keterbatasan dan disclaimer")
st.markdown(
    "- Data historis (2015-2017) dari konteks hotel tertentu; pola belum tentu berlaku untuk hotel, negara, "
    "atau periode lain.\n"
    "- Model mempelajari pola statistik, **bukan alasan pasti** seseorang membatalkan reservasi.\n"
    "- Pembatalan mendadak (pemesanan dekat dengan tanggal kedatangan) sulit dideteksi.\n"
    "- Probabilitas adalah estimasi; sebagian reservasi yang tidak batal juga ditandai berpotensi batal.\n"
    "- Hasil prediksi tidak boleh menjadi satu-satunya dasar untuk menolak, membatalkan, atau memperlakukan "
    "pelanggan secara berbeda.\n"
    "- Aplikasi ini prototipe edukasi, bukan sistem operasional hotel.")

st.subheader("Tim")
st.write("Isi nama anggota, NIM, kelas, dan pembagian tugas di sini sebelum dikumpulkan.")
