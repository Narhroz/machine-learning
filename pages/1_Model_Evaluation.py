"""Halaman evaluasi model (FR-08)."""
import pandas as pd
import streamlit as st
from utils import require_artifact, REPORTS, FIGURES, read_json

st.set_page_config(page_title="Model Evaluation", page_icon="📊", layout="wide")
artifact = require_artifact()
cfg = read_json(REPORTS / "preprocessing_config.json")

st.title("📊 Evaluasi Model")

# ---- Ringkasan data ----
st.subheader("Ringkasan data")
c1, c2, c3 = st.columns(3)
c1.metric("Data latih", f"{cfg.get('n_train', '-'):,}" if cfg else "-")
c2.metric("Data uji", f"{cfg.get('n_test', '-'):,}" if cfg else "-")
c3.metric("Model final", artifact["model_name"])
st.caption("Dataset Hotel Booking Demand setelah baris duplikat dihapus. Pembagian data 80:20 (stratified, "
           "random_state=42). Data uji hanya dipakai sekali untuk evaluasi akhir.")

# ---- Perbandingan model ----
st.subheader("Perbandingan tiga model (data uji)")
path = REPORTS / "model_comparison.csv"
if path.exists():
    tbl = pd.read_csv(path, index_col=[0, 1])
    sel = tbl[tbl.index.get_level_values(1).str.contains("OOF")].droplevel(1)
    st.write(f"Threshold dipilih dari prediksi out-of-fold pada data latih (≈{artifact['threshold']:.2f}).")
    st.dataframe(sel.style.format("{:.3f}").highlight_max(axis=0, color="#cfe8ff"))
    with st.expander("Lihat juga hasil dengan threshold 0,5"):
        st.dataframe(tbl[~tbl.index.get_level_values(1).str.contains("OOF")].droplevel(1)
                     .style.format("{:.3f}"))
    st.caption("Sel yang disorot adalah nilai tertinggi per kolom. Accuracy bukan satu-satunya dasar pemilihan "
               "model; Recall dan PR-AUC kelas batal diutamakan.")
else:
    st.info("`reports/model_comparison.csv` belum ada. Jalankan notebook 05 lalu salin folder `reports/`.")

# ---- Grafik ----
def show(fname, title, text):
    p = FIGURES / fname
    st.subheader(title)
    if p.exists():
        st.image(str(p))
    else:
        st.info(f"Gambar `{fname}` belum ada di `reports/figures/`.")
    st.caption(text)

show("confusion_matrices.png", "Confusion matrix",
     "Baris = kelas sebenarnya, kolom = prediksi. False Negative adalah pembatalan yang terlewat; "
     "False Positive adalah peringatan keliru.")
show("roc_pr_curves.png", "Kurva ROC dan Precision-Recall",
     "Semakin ke kiri-atas (ROC) dan semakin ke kanan-atas (PR) semakin baik. Garis putus-putus pada kurva PR "
     "adalah proporsi pembatalan sebagai pembanding acak.")
show("threshold_selection.png", "Pemilihan threshold",
     "Menurunkan threshold menaikkan Recall tetapi menurunkan Precision. Garis putus-putus menandai threshold "
     "dengan F1 tertinggi pada data latih.")
show("permutation_importance.png", "Pengaruh fitur",
     "Penurunan PR-AUC saat fitur diacak. Menunjukkan fitur yang paling dipakai model, bukan hubungan sebab-akibat.")
show("calibration.png", "Kalibrasi probabilitas",
     "Semakin dekat ke garis diagonal, semakin sesuai probabilitas prediksi dengan proporsi pembatalan sebenarnya.")
