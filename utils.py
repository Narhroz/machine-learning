"""Fungsi bantu untuk aplikasi Hotel Booking Cancellation Prediction."""
from pathlib import Path
import json
import joblib
import pandas as pd
import streamlit as st

BASE = Path(__file__).resolve().parent
MODEL_PATH = BASE / "models" / "final_model.joblib"
REPORTS = BASE / "reports"
FIGURES = REPORTS / "figures"

# Rentang input yang diizinkan (sesuai data latih)
LEAD_MIN, LEAD_MAX = 0, 740
REQ_MIN, REQ_MAX = 0, 5

COUNTRY_NAMES = {
    "PRT": "Portugal", "GBR": "Inggris", "FRA": "Prancis", "ESP": "Spanyol", "DEU": "Jerman",
    "ITA": "Italia", "IRL": "Irlandia", "BEL": "Belgia", "BRA": "Brasil", "NLD": "Belanda",
}
OTHER_COUNTRY = "OTHER"  # negara di luar daftar -> masuk kategori "lainnya" pada pipeline

SEGMENT_LABELS = {
    "Online TA": "Agen travel online (Online TA)",
    "Offline TA/TO": "Agen travel / tour operator offline",
    "Direct": "Langsung ke hotel",
    "Groups": "Rombongan / grup",
    "Corporate": "Perusahaan (Corporate)",
    "Complementary": "Gratis / komplimen",
    "Aviation": "Maskapai penerbangan",
}
CUSTOMER_LABELS = {
    "Transient": "Individu / perorangan (Transient)",
    "Transient-Party": "Rombongan kecil perorangan (Transient-Party)",
    "Contract": "Kontrak",
    "Group": "Grup",
}


@st.cache_resource(show_spinner="Memuat model...")
def load_artifact():
    """Memuat pipeline + threshold yang disimpan dari notebook 05. None jika file belum ada."""
    if not MODEL_PATH.exists():
        return None
    return joblib.load(MODEL_PATH)


def require_artifact():
    art = load_artifact()
    if art is None:
        st.error(
            "File model `models/final_model.joblib` belum ditemukan. Jalankan notebook "
            "`05_model_evaluation.ipynb`, lalu salin folder `models/` dan `reports/` ke folder aplikasi ini."
        )
        st.stop()
    return art


def known_countries(artifact):
    """Daftar negara yang punya kolom sendiri di pipeline (hasil pelatihan)."""
    try:
        oh = artifact["pipeline"].named_steps["prep"].named_transformers_["country"].named_steps["oh"]
        infreq = oh.infrequent_categories_[0]
        kept = [c for c in oh.categories_[0] if infreq is None or c not in infreq]
        kept = [c for c in kept if c != "Unknown"]
        if kept:
            return sorted(kept, key=lambda c: COUNTRY_NAMES.get(c, c))
    except Exception:
        pass
    return sorted(COUNTRY_NAMES, key=lambda c: COUNTRY_NAMES[c])


def validate_inputs(d, countries):
    """FR-02: mengembalikan daftar pesan kesalahan (kosong jika valid)."""
    errors = []
    lt, rq = d.get("lead_time"), d.get("total_of_special_requests")
    if lt is None or not (LEAD_MIN <= lt <= LEAD_MAX):
        errors.append(f"Jarak pemesanan harus berupa angka {LEAD_MIN}-{LEAD_MAX} hari.")
    if rq is None or not (REQ_MIN <= rq <= REQ_MAX):
        errors.append(f"Jumlah permintaan khusus harus {REQ_MIN}-{REQ_MAX}.")
    if d.get("country") not in set(countries) | {OTHER_COUNTRY}:
        errors.append("Negara asal tamu belum dipilih dengan benar.")
    if d.get("market_segment") not in SEGMENT_LABELS:
        errors.append("Asal pemesanan belum dipilih dengan benar.")
    if d.get("customer_type") not in CUSTOMER_LABELS:
        errors.append("Tipe pelanggan belum dipilih dengan benar.")
    return errors


def predict(artifact, inputs):
    """Input mentah -> probabilitas batal dan label. Preprocessing dilakukan oleh pipeline tersimpan."""
    row = pd.DataFrame([inputs])[artifact["features"]]
    proba = float(artifact["pipeline"].predict_proba(row)[0, 1])
    label = int(proba >= artifact["threshold"])
    return proba, label


def read_json(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:
        return {}


def cancel_rate_pct(default=27.0):
    """Persentase pembatalan setelah duplikat dibuang (dari reports/data_audit_summary.csv, hasil notebook 01)."""
    try:
        df = pd.read_csv(REPORTS / "data_audit_summary.csv", index_col=0)
        return float(df.loc["rasio_batal_dedup_%"].iloc[0])
    except Exception:
        return default
