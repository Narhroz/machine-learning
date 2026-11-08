# Hotel Booking Cancellation Prediction

Aplikasi Streamlit untuk memperkirakan apakah reservasi hotel berpotensi dibatalkan.
Proyek akhir MK Pembelajaran Mesin 2026 (Sekolah Vokasi, Teknologi Rekayasa Komputer).

**Dataset:** Hotel Booking Demand (Kaggle `jessemostipak/hotel-booking-demand`; Antonio, de Almeida & Nunes, 2019, https://doi.org/10.1016/j.dib.2018.11.126)
**Model:** Logistic Regression, Random Forest, XGBoost dibandingkan; model final dimuat dari `models/final_model.joblib`.
**Input aplikasi (5):** jarak pemesanan ke kedatangan, negara asal tamu, asal pemesanan, jumlah permintaan khusus, tipe pelanggan.

## Struktur
```text
app.py                       halaman prediksi
pages/1_Model_Evaluation.py  perbandingan model, confusion matrix, kurva
pages/2_About_Project.py     latar belakang, dataset, keterbatasan
utils.py                     fungsi bantu (muat model, validasi, prediksi)
ui.py                        tampilan bersama (CSS, navigasi, nama brand, daftar tim)
.streamlit/config.toml       tema warna dan pengaturan tampilan
models/final_model.joblib    dihasilkan notebook 05
reports/                     model_comparison.csv, preprocessing_config.json, figures/ (dihasilkan notebook 03 dan 05)
notebooks/                   01_data_understanding ... 05_model_evaluation
tests/test_app.py            unit test fungsi bantu + smoke test halaman Streamlit
requirements.txt
```

## Cara menjalankan
1. Jalankan notebook `03_preprocessing` dan `05_model_evaluation` sampai selesai (dataset `hotel_bookings.csv` dari Kaggle).
2. Salin folder `models/` dan `reports/` hasil notebook ke folder aplikasi ini.
3. Pasang dependensi, lalu jalankan:
```bash
pip install -r requirements.txt
streamlit run app.py
```
4. Untuk menjalankan pengujian otomatis (validasi input, faktor pendorong lokal, dan smoke test ketiga halaman):
```bash
python -m unittest discover -s tests -v
```

**Penting:** jalankan aplikasi di environment Python yang sama dengan yang dipakai melatih model (versi scikit-learn dan xgboost harus sama saat memuat file `.joblib`). Kunci versinya dengan `pip freeze > requirements.txt`.

## Mengubah tampilan
- Nama brand dan nama anggota tim: edit `BRAND` dan `TEAM` di bagian atas `ui.py`.
- Warna dan font: variabel CSS di `ui.py` (`--ink`, `--lagoon`, `--brass`).
- Font memakai Google Fonts, sehingga butuh internet; tanpa internet tampilan memakai font bawaan sistem.

## Catatan
- Hasil adalah estimasi model, bukan kepastian pembatalan. Aplikasi ini prototipe edukasi.
- Dataset mentah tidak disertakan; unduh dari Kaggle sesuai ketentuan lisensinya.
