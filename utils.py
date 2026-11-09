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


SEGMENT_CANCEL_PCT = {
    "Online TA": 35.2,
    "Groups": 27.1,
    "Aviation": 22.1,
    "Direct": 14.7,
    "Offline TA/TO": 14.6,
    "Complementary": 12.2,
    "Corporate": 11.9,
}

REQUEST_CANCEL_PCT = {0: 32.9, 1: 18.2, 2: 17.8, 3: 17.1, 4: 13.8, 5: 11.4}


def lead_bucket_benchmark(lead_days):
    """Rasio batal historis (%) untuk kelompok jarak pemesanan (notebook 02)."""
    d = int(lead_days)
    if d <= 7:
        return "Jarak 0-7 hari", 8.4
    if d <= 30:
        return "Jarak 8-30 hari", 25.3
    if d <= 90:
        return "Jarak 31-90 hari", 31.8
    if d <= 180:
        return "Jarak 91-180 hari", 34.7
    if d <= 365:
        return "Jarak 181-365 hari", 39.3
    return "Jarak >365 hari", 42.0


def historical_benchmarks(inputs, proba):
    """Data bar komparasi antara prediksi booking ini dan rata-rata historis segmen/fitur."""
    lt_label, lt_pct = lead_bucket_benchmark(inputs.get("lead_time", 60))
    seg = inputs.get("market_segment", "Online TA")
    seg_pct = SEGMENT_CANCEL_PCT.get(seg, 27.3)
    req = int(inputs.get("total_of_special_requests", 0))
    req_pct = REQUEST_CANCEL_PCT.get(req, 15.0)
    base_pct = round(cancel_rate_pct(), 1)
    return [
        {"Kategori": "Prediksi booking ini", "Peluang batal (%)": round(float(proba) * 100.0, 1), "Tipe": "Prediksi"},
        {"Kategori": f"Historis {lt_label}", "Peluang batal (%)": lt_pct, "Tipe": "Historis"},
        {"Kategori": f"Historis segmen {seg}", "Peluang batal (%)": seg_pct, "Tipe": "Historis"},
        {"Kategori": f"Historis {req} permintaan khusus", "Peluang batal (%)": req_pct, "Tipe": "Historis"},
        {"Kategori": "Rata-rata seluruh data", "Peluang batal (%)": base_pct, "Tipe": "Rata-rata"},
    ]


def operational_recommendations(proba, threshold, inputs):
    """Rekomendasi langkah operasional hotel & stamp status berdasarkan skor risiko dan profil booking."""
    p = float(proba)
    thr = float(threshold)
    lt = int(inputs.get("lead_time", 0))
    req = int(inputs.get("total_of_special_requests", 0))
    seg = inputs.get("market_segment", "Online TA")

    if p >= thr + 0.15:
        stamp = ("HIGH RISK · TINDAKAN AKTIF", "stamp-risk")
        actions = [
            "Kirim konfirmasi ulang otomatis (WhatsApp/email) pada H-14 dan H-3 sebelum check-in.",
            "Terapkan kebijakan deposit sebagian atau batas waktu pembatalan gratis (free-cancellation) lebih awal.",
            "Alokasikan kamar ke kuota cadangan (buffer overbooking terukur) jika dipesan lewat kanal Online TA.",
        ]
    elif p >= thr:
        stamp = ("WATCHLIST · PANTAU KONFIRMASI", "stamp-watch")
        actions = [
            "Kirim pesan pengingat ramah H-7 berisi ringkasan fasilitas dan opsi permintaan khusus (misal pilih lantai/tipe bantal).",
            "Minta konfirmasi perkiraan jam kedatangan (estimated arrival time) untuk menguji komitmen tamu.",
            "Tawarkan insentif kecil jika tamu mengubah reservasi ke paket non-refundable.",
        ]
    else:
        stamp = ("SECURE BOOKING · SIAPKAN LAYANAN", "stamp-safe")
        actions = [
            "Reservasi relatif aman; prioritaskan persiapan kamar sesuai preferensi tamu.",
            "Tawarkan program upselling pra-kedatangan (paket sarapan, upgrade kamar, atau penjemputan bandara).",
            "Jika tamu memesan jauh hari, kirim panduan wisata lokal H-3 untuk meningkatkan pengalaman menginap.",
        ]

    if req == 0 and p >= thr:
        actions.append("Tamu belum mencatat permintaan khusus — tanyakan preferensi kamar singkat agar keterikatan reservasi meningkat.")
    elif lt > 120 and seg == "Online TA":
        actions.append("Jarak pesan >4 bulan via Online TA memiliki histori batal tinggi — jadwalkan verifikasi kartu/metode pembayaran.")
    return stamp, actions[:3]


def what_if_scenarios(artifact, inputs):
    """Simulasi sensitivitas 'Bagaimana jika...' terhadap perubahan 1 fitur kunci."""
    curr_proba, _ = predict(artifact, inputs)
    curr_pct = curr_proba * 100.0
    scenarios = []

    req = int(inputs.get("total_of_special_requests", 0))
    if req < REQ_MAX:
        alt = dict(inputs, total_of_special_requests=min(REQ_MAX, req + 2))
        p_alt, _ = predict(artifact, alt)
        scenarios.append({
            "Skenario": f"Tamu menambah permintaan khusus ({req} → {alt['total_of_special_requests']})",
            "Peluang Baru (%)": round(p_alt * 100.0, 1),
            "Perubahan (poin %)": round(p_alt * 100.0 - curr_pct, 1),
        })
    else:
        alt = dict(inputs, total_of_special_requests=0)
        p_alt, _ = predict(artifact, alt)
        scenarios.append({
            "Skenario": f"Permintaan khusus dihapus ({req} → 0)",
            "Peluang Baru (%)": round(p_alt * 100.0, 1),
            "Perubahan (poin %)": round(p_alt * 100.0 - curr_pct, 1),
        })

    seg = inputs.get("market_segment", "Online TA")
    target_seg = "Direct" if seg != "Direct" else "Online TA"
    alt_seg = dict(inputs, market_segment=target_seg)
    p_seg, _ = predict(artifact, alt_seg)
    scenarios.append({
        "Skenario": f"Kanal pesan diubah ({seg} → {target_seg})",
        "Peluang Baru (%)": round(p_seg * 100.0, 1),
        "Perubahan (poin %)": round(p_seg * 100.0 - curr_pct, 1),
    })

    lt = int(inputs.get("lead_time", 60))
    target_lt = 14 if lt > 21 else 150
    alt_lt = dict(inputs, lead_time=target_lt)
    p_lt, _ = predict(artifact, alt_lt)
    scenarios.append({
        "Skenario": f"Jarak pemesanan diubah ({lt} hari → {target_lt} hari)",
        "Peluang Baru (%)": round(p_lt * 100.0, 1),
        "Perubahan (poin %)": round(p_lt * 100.0 - curr_pct, 1),
    })

    cust = inputs.get("customer_type", "Transient")
    target_cust = "Transient-Party" if cust == "Transient" else "Transient"
    alt_cust = dict(inputs, customer_type=target_cust)
    p_cust, _ = predict(artifact, alt_cust)
    scenarios.append({
        "Skenario": f"Tipe tamu diubah ({cust} → {target_cust})",
        "Peluang Baru (%)": round(p_cust * 100.0, 1),
        "Perubahan (poin %)": round(p_cust * 100.0 - curr_pct, 1),
    })
    return scenarios


def sample_batch_dataframe():
    """Contoh dataset CSV (8 baris) untuk simulasi prediksi batch."""
    return pd.DataFrame([
        {"lead_time": 210, "country": "PRT", "market_segment": "Online TA", "total_of_special_requests": 0, "customer_type": "Transient"},
        {"lead_time": 12, "country": "GBR", "market_segment": "Direct", "total_of_special_requests": 2, "customer_type": "Transient-Party"},
        {"lead_time": 95, "country": "FRA", "market_segment": "Online TA", "total_of_special_requests": 1, "customer_type": "Transient"},
        {"lead_time": 4, "country": "DEU", "market_segment": "Corporate", "total_of_special_requests": 1, "customer_type": "Contract"},
        {"lead_time": 165, "country": "ESP", "market_segment": "Groups", "total_of_special_requests": 0, "customer_type": "Group"},
        {"lead_time": 38, "country": "ITA", "market_segment": "Online TA", "total_of_special_requests": 3, "customer_type": "Transient"},
        {"lead_time": 280, "country": "PRT", "market_segment": "Offline TA/TO", "total_of_special_requests": 0, "customer_type": "Transient"},
        {"lead_time": 19, "country": "NLD", "market_segment": "Direct", "total_of_special_requests": 2, "customer_type": "Transient"},
    ])


def predict_batch(artifact, df, countries):
    """Menjalankan prediksi batch pada DataFrame yang memiliki 5 kolom fitur."""
    req_cols = list(artifact["features"])
    missing = [c for c in req_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Kolom wajib belum ada di CSV: {', '.join(missing)}")
    work = df.copy()
    work["lead_time"] = pd.to_numeric(work["lead_time"], errors="coerce").fillna(30).clip(LEAD_MIN, LEAD_MAX).astype(int)
    work["total_of_special_requests"] = (
        pd.to_numeric(work["total_of_special_requests"], errors="coerce").fillna(0).clip(REQ_MIN, REQ_MAX).astype(int)
    )
    valid_countries = set(countries) | {OTHER_COUNTRY}
    work["country"] = work["country"].astype(str).str.strip().str.upper()
    work["country"] = work["country"].apply(lambda c: c if c in valid_countries else OTHER_COUNTRY)
    work["market_segment"] = work["market_segment"].astype(str).str.strip()
    work["market_segment"] = work["market_segment"].apply(lambda s: s if s in SEGMENT_LABELS else "Online TA")
    work["customer_type"] = work["customer_type"].astype(str).str.strip()
    work["customer_type"] = work["customer_type"].apply(lambda c: c if c in CUSTOMER_LABELS else "Transient")

    probas = artifact["pipeline"].predict_proba(work[req_cols])[:, 1]
    thr = float(artifact["threshold"])
    out = work[req_cols].copy()
    out["Peluang Batal (%)"] = (probas * 100.0).round(1)
    out["Status Prediksi"] = ["Berpotensi batal" if p >= thr else "Tidak berpotensi batal" for p in probas]
    return out
