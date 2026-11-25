# StayCheck: Prediksi Pembatalan Booking Hotel

Proyek Akhir Mata Kuliah Pembelajaran Mesin (TEK1302) 2026, Sekolah Vokasi IPB, Teknologi Rekayasa Komputer.

StayCheck adalah aplikasi web (Streamlit) yang memperkirakan apakah sebuah reservasi hotel berpotensi dibatalkan, berdasarkan 10 informasi reservasi. Model dilatih pada dataset Hotel Booking Demand (City Hotel Lisbon dan Resort Hotel Algarve, 2015-2017).

> Prototipe edukasi. Hasil prediksi adalah estimasi, bukan kepastian, dan tidak boleh menjadi satu-satunya dasar untuk menolak atau memperlakukan pelanggan secara berbeda.

- **Kelas / Kelompok:** B / Kelompok 9
- **Link aplikasi:** https://staypredict.streamlit.app/

## Anggota

| Nama | NIM | Peran |
|---|---|---|
| Nala Arham Rozana | J0404241077 | Data: dataset, EDA, preprocessing (notebook 01-03) |
| Ammar Hudzafah | J0404241026 | Model: training, tuning, evaluasi (notebook 04-05) |
| Deandra Aidila Hidayat | J0404241146 | Aplikasi: Streamlit, integrasi pipeline, dokumentasi |

## Ringkasan

| Aspek | Isi |
|---|---|
| Jenis | Supervised learning, klasifikasi biner (target `is_canceled`) |
| Dataset | Hotel Booking Demand (Antonio, de Almeida & Nunes, 2019), 119.390 baris mentah, 87.151 setelah duplikat dibuang |
| Fitur (10) | `lead_time`, `country`, `market_segment`, `total_of_special_requests`, `customer_type`, `hotel`, `nights`, `adr`, `previous_cancellations`, `is_repeated_guest` |
| Algoritma dibandingkan | Logistic Regression, Random Forest, XGBoost |
| Split | 80:20 stratified, `random_state=42` (train 69.720, test 17.431) |
| Model final | XGBoost, threshold 0,322 (dipilih dari prediksi out-of-fold pada data train) |

**Hasil pada data uji (dievaluasi satu kali):**

| Model | Threshold | Accuracy | Precision | Recall | F1 | ROC-AUC | PR-AUC |
|---|---|---|---|---|---|---|---|
| Logistic Regression | 0,289 | 0,741 | 0,518 | 0,742 | 0,610 | 0,817 | 0,620 |
| Random Forest | 0,313 | 0,781 | 0,576 | 0,742 | 0,649 | 0,858 | 0,703 |
| **XGBoost (final)** | **0,322** | **0,788** | **0,587** | **0,754** | **0,660** | **0,864** | **0,712** |

Model dipilih berdasarkan PR-AUC validasi silang tertinggi pada data train dan Recall kelas batal, bukan Accuracy saja. Detail analisis ada di halaman **Evaluasi model** pada aplikasi dan di `PRD.md` bagian 7.8.

## Fitur aplikasi

- Form prediksi 10 input (slider + kotak ketik, dropdown) dan 6 skenario cepat.
- Hasil: kelas prediksi, probabilitas, posisi terhadap threshold, 3 faktor pendorong utama.
- Grafik pembanding dengan rata-rata historis, rekomendasi operasional, kalkulator dampak finansial, simulator "bagaimana jika".
- Prediksi banyak reservasi sekaligus (unggah CSV atau 8 sampel) dan riwayat sesi.
- Halaman Evaluasi model dan Tentang proyek.

Catatan: rekomendasi operasional, saran deposit 25%/50%, dan benchmark historis adalah heuristik/asumsi, bukan keluaran model terlatih.

## Struktur folder

```text
hotel-booking-cancellation/
├── app.py                      # beranda + prediksi
├── ui.py                       # CSS, navigasi, komponen tampilan
├── utils.py                    # validasi, prediksi, penjelasan, simulasi
├── pages/
│   ├── 1_Model_Evaluation.py
│   └── 2_About_Project.py
├── assets/team/                # foto anggota (opsional)
├── data/
│   ├── raw/                    # taruh hotel_bookings.csv di sini (tidak disertakan)
│   └── processed/              # train.csv, test.csv (hasil notebook 03)
├── models/final_model.joblib   # pipeline + model + threshold
├── notebooks/                  # 01_data_understanding ... 05_model_evaluation
├── reports/                    # figures/, model_comparison.csv, preprocessing_config.json, data_audit_summary.csv
├── requirements.txt
└── README.md
```

## Menjalankan aplikasi

Versi online tersedia di https://staypredict.streamlit.app/. Untuk menjalankan lokal, butuh Python 3.10 atau lebih baru dan koneksi internet (foto hotel di beranda dimuat dari Unsplash).

```bash
# 1. Masuk ke folder proyek
cd hotel-booking-cancellation

# 2. Buat dan aktifkan virtual environment
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Pasang dependensi
pip install -r requirements.txt

# 4. Jalankan
streamlit run app.py
```

Aplikasi terbuka di `http://localhost:8501`. Pastikan folder `models/` dan `reports/` ikut ada; tanpa `models/final_model.joblib` aplikasi menampilkan pesan error.

**Versi library:** model disimpan dengan scikit-learn versi tertentu. Model dilatih dengan scikit-learn 1.9.0 dan xgboost 3.4.1; keduanya dikunci di `requirements.txt` agar tidak muncul `InconsistentVersionWarning`.

## Mengulang eksperimen (notebook)

1. Unduh `hotel_bookings.csv` dari [Kaggle: Hotel Booking Demand](https://www.kaggle.com/datasets/jessemostipak/hotel-booking-demand) dan simpan di `data/raw/`.
2. Pasang paket tambahan: `pip install matplotlib seaborn jupyter`.
3. Jalankan notebook berurutan dari **folder utama proyek** sebagai working directory (notebook memakai path relatif seperti `data/processed` dan `reports`; notebook awalnya dikembangkan di Kaggle):

| Notebook | Isi | Keluaran utama |
|---|---|---|
| `01_data_understanding` | Audit data | `reports/data_audit_summary.csv` |
| `02_eda` | EDA dan visualisasi | `reports/figures/*.png` |
| `03_preprocessing` | Hapus duplikat, split, pipeline | `data/processed/`, `reports/preprocessing_config.json` |
| `04_model_training` | Baseline 3 model, validasi 5 vs 10 fitur | tabel CV |
| `05_model_evaluation` | Tuning, threshold, evaluasi test, analisis | `models/final_model.joblib`, `reports/` |

## Catatan metodologi

- Duplikat dihapus **sebelum** split; semua transformasi dipelajari hanya dari data train (satu `Pipeline`).
- `reservation_status`, `reservation_status_date`, dan `required_car_parking_spaces` tidak dipakai karena leakage.
- Test set tidak dipakai untuk memilih fitur, threshold, atau hyperparameter.
- Data dibagi acak (bukan berdasarkan waktu), sehingga performa pada periode yang lebih baru belum teruji.
- Pembatalan mendadak (lead time ≤ 7 hari) sulit dideteksi (Recall 0,22).
- `country`, `previous_cancellations`, dan `is_repeated_guest` hanya dipakai karena berkorelasi dengan pola di data historis, bukan untuk membedakan perlakuan terhadap tamu.
- Tarif (`adr`) dalam euro, tingkat harga Portugal 2015-2017.

## Sumber dan atribusi

- Dataset: Antonio, N., de Almeida, A., & Nunes, L. (2019). Hotel booking demand datasets. *Data in Brief*, 22, 41-49. https://doi.org/10.1016/j.dib.2018.11.126
- Foto ilustrasi hotel di beranda: [Unsplash](https://unsplash.com) (bukan foto hotel pada dataset).
