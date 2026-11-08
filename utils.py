"""Fungsi bantu untuk aplikasi Hotel Booking Cancellation Prediction."""
from pathlib import Path
import json
import math
import warnings
import joblib
import pandas as pd
import streamlit as st
from sklearn.exceptions import InconsistentVersionWarning

warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

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
    """Memuat pipeline + threshold yang disimpan dari notebook 05. None jika file belum ada atau rusak."""
    if not MODEL_PATH.exists():
        return None
    try:
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=InconsistentVersionWarning)
            art = joblib.load(MODEL_PATH)
    except Exception:
        return None
    required = {"pipeline", "model_name", "threshold", "features"}
    if not isinstance(art, dict) or not required.issubset(art):
        return None
    return art


def require_artifact():
    art = load_artifact()
    if art is None:
        st.error(
            "File model `models/final_model.joblib` belum ditemukan atau tidak dapat dibaca. "
            "Jalankan notebook `05_model_evaluation.ipynb`, lalu salin folder `models/` dan `reports/` ke folder aplikasi ini."
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


def _int_or_none(v):
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, float) and (math.isnan(v) or math.isinf(v) or not v.is_integer()):
        return None
    try:
        return int(v)
    except (TypeError, ValueError):
        return None


def validate_inputs(d, countries):
    """FR-02: mengembalikan daftar pesan kesalahan (kosong jika valid)."""
    errors = []
    if not isinstance(d, dict):
        return ["Data input tidak valid."]
    lt, rq = _int_or_none(d.get("lead_time")), _int_or_none(d.get("total_of_special_requests"))
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


FEATURE_TITLES = {
    "lead_time": "Jarak pemesanan",
    "country": "Negara asal tamu",
    "market_segment": "Asal pemesanan",
    "total_of_special_requests": "Permintaan khusus",
    "customer_type": "Tipe pelanggan",
}


def format_input_value(feature, value):
    """Format nilai input menjadi teks ramah pengguna."""
    if feature == "lead_time":
        return f"{int(value)} hari sebelum menginap"
    if feature == "country":
        return "Negara lain" if value == OTHER_COUNTRY else f"{COUNTRY_NAMES.get(value, value)} ({value})"
    if feature == "market_segment":
        return SEGMENT_LABELS.get(value, str(value))
    if feature == "total_of_special_requests":
        return f"{int(value)} permintaan khusus"
    if feature == "customer_type":
        return CUSTOMER_LABELS.get(value, str(value))
    return str(value)


def explain_local_drivers(artifact, inputs, baseline=None):
    """Kontribusi lokal tiap fitur dengan membandingkan prediksi terhadap profil acuan."""
    base = dict(
        baseline or {
            "lead_time": 60,
            "country": "PRT",
            "market_segment": "Online TA",
            "total_of_special_requests": 0,
            "customer_type": "Transient",
        }
    )
    feats = list(artifact["features"])
    curr_proba, _ = predict(artifact, inputs)
    rows = []
    for f in feats:
        perturbed = dict(inputs)
        perturbed[f] = base.get(f, inputs[f])
        alt_proba, _ = predict(artifact, perturbed)
        delta_pp = (curr_proba - alt_proba) * 100.0
        rows.append(
            {
                "feature": f,
                "title": FEATURE_TITLES.get(f, f),
                "value": format_input_value(f, inputs[f]),
                "delta_pp": delta_pp,
            }
        )
    rows.sort(key=lambda r: abs(r["delta_pp"]), reverse=True)
    return rows


def threshold_zone(proba, threshold):
    """Mengembalikan (kode_zona, teks_penjelasan) posisi probabilitas terhadap threshold."""
    diff_pp = (float(proba) - float(threshold)) * 100.0
    if abs(diff_pp) < 5.0:
        return "near", f"Mendekati batas ({diff_pp:+.1f} poin dari batas {threshold*100:.0f}%)"
    if diff_pp >= 15.0:
        return "high", f"Jauh di atas batas ({diff_pp:+.1f} poin dari batas {threshold*100:.0f}%)"
    if diff_pp >= 5.0:
        return "above", f"Di atas batas ({diff_pp:+.1f} poin dari batas {threshold*100:.0f}%)"
    if diff_pp <= -15.0:
        return "low", f"Jauh di bawah batas ({diff_pp:+.1f} poin dari batas {threshold*100:.0f}%)"
    return "below", f"Di bawah batas ({diff_pp:+.1f} poin dari batas {threshold*100:.0f}%)"


def read_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception:
        return {}


def cancel_rate_pct(default=27.0):
    """Persentase pembatalan setelah duplikat dibuang (dari reports/data_audit_summary.csv, hasil notebook 01)."""
    try:
        df = pd.read_csv(REPORTS / "data_audit_summary.csv", index_col=0)
        return float(df.loc["rasio_batal_dedup_%"].iloc[0])
    except Exception:
        return default
