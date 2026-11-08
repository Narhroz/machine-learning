"""Evaluasi model (FR-08), tampilan ringkas dengan tab."""
import pandas as pd
import streamlit as st
from ui import inject_css, top_nav, html, BRAND, FAVICON
from utils import require_artifact, REPORTS, FIGURES, read_json

st.set_page_config(page_title=f"{BRAND} - Evaluasi model", page_icon=FAVICON, layout="wide")
inject_css()
artifact = require_artifact()
cfg = read_json(REPORTS / "preprocessing_config.json")
NAMES = {"LogReg": "Logistic Regression", "RandomForest": "Random Forest", "XGBoost": "XGBoost"}
m = artifact.get("metrics_test", {})
thr = artifact["threshold"]

top_nav()
html("""<section class="hero" style="grid-template-columns:1fr;padding-bottom:0"><div>
<h1 style="font-size:2.8rem">Seberapa jago modelnya?</h1>
<p class="lead">Tiga algoritma dilatih pada data yang sama, lalu diuji sekali pada data yang disimpan terpisah. Di sini kamu bisa lihat siapa yang menang dan di mana model masih sering salah.</p></div></section>""")

k = st.columns(4)
k[0].metric("Model terpilih", NAMES.get(artifact["model_name"], artifact["model_name"]))
k[1].metric("Data latih", f"{cfg['n_train']:,}" if cfg.get("n_train") else "-")
k[2].metric("Data uji", f"{cfg['n_test']:,}" if cfg.get("n_test") else "-")
k[3].metric("Batas penandaan", f"{thr*100:.0f}%")
st.caption("Pembagian data 80:20 (stratified, random_state=42) setelah baris duplikat dibuang. Data uji hanya dipakai sekali untuk evaluasi akhir.")
if not cfg:
    st.warning("File `reports/preprocessing_config.json` belum ada atau gagal dibaca, sehingga jumlah data latih/uji tidak dapat ditampilkan.")


def show(fname, title, text):
    st.markdown(f"### {title}")
    p = FIGURES / fname
    if p.exists():
        st.image(str(p))
    else:
        st.info(f"Gambar `{fname}` belum ada di `reports/figures/`. Jalankan notebook 05 lalu salin folder `reports/`.")
    st.caption(text)


t1, t2, t3, t4 = st.tabs(["Perbandingan model", "Kesalahan model", "Kurva dan batas", "Fitur dan kalibrasi"])

with t1:
    path = REPORTS / "model_comparison.csv"
    if path.exists():
        try:
            tbl = pd.read_csv(path, index_col=[0, 1])
            is_oof = tbl.index.get_level_values(1).str.contains("OOF")
            st.markdown("### Hasil pada data uji")
            st.write(f"Batas penandaan ≈{thr*100:.0f}% dipilih dari prediksi out-of-fold pada data latih, bukan dari data uji.")
            st.dataframe(tbl[is_oof].droplevel(1).rename(index=NAMES).style.format("{:.3f}").highlight_max(axis=0, color="#FBE3A6"))
            st.caption("Sel kuning = nilai tertinggi per kolom. Accuracy bukan satu-satunya dasar memilih model; "
                       "Recall dan PR-AUC kelas batal diutamakan karena tujuan utamanya menemukan pembatalan.")
            with st.expander("Lihat juga hasil dengan batas 50%"):
                st.dataframe(tbl[~is_oof].droplevel(1).rename(index=NAMES).style.format("{:.3f}"))
        except Exception:
            st.error("File `reports/model_comparison.csv` ditemukan tetapi formatnya tidak dapat dibaca.")
    else:
        st.info("`reports/model_comparison.csv` belum ada. Jalankan notebook 05 lalu salin folder `reports/`.")
with t2:
    show("confusion_matrices.png", "Confusion matrix",
         "Baris = kondisi sebenarnya, kolom = tebakan model. False Negative adalah pembatalan yang terlewat; "
         "False Positive adalah peringatan keliru.")
with t3:
    show("roc_pr_curves.png", "Kurva ROC dan Precision-Recall",
         "Makin ke kiri-atas (ROC) dan makin ke kanan-atas (PR), makin bagus. Garis putus-putus pada kurva PR "
         "adalah proporsi pembatalan, yaitu hasil kalau menebak acak.")
    show("threshold_selection.png", "Memilih batas penandaan",
         "Menurunkan batas menaikkan Recall tetapi menurunkan Precision. Garis putus-putus menandai batas dengan F1 tertinggi pada data latih.")
with t4:
    show("permutation_importance.png", "Fitur yang paling dipakai model",
         "Penurunan PR-AUC saat satu fitur diacak. Ini menunjukkan fitur yang paling dipakai model, bukan hubungan sebab-akibat.")
    show("calibration.png", "Apakah persentasenya masuk akal?",
         "Makin dekat ke garis diagonal, makin sesuai persentase prediksi dengan proporsi pembatalan sebenarnya.")
