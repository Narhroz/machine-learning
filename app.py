"""Hotel Booking Cancellation Prediction - halaman prediksi (Streamlit)."""
import streamlit as st
from utils import (load_artifact, require_artifact, known_countries, validate_inputs, predict,
                   COUNTRY_NAMES, OTHER_COUNTRY, SEGMENT_LABELS, CUSTOMER_LABELS,
                   LEAD_MIN, LEAD_MAX, REQ_MIN, REQ_MAX)

st.set_page_config(page_title="Prediksi Pembatalan Booking Hotel", page_icon="🏨", layout="centered")

artifact = require_artifact()
countries = known_countries(artifact)
country_options = countries + [OTHER_COUNTRY]
country_fmt = lambda c: "Negara lain" if c == OTHER_COUNTRY else f"{COUNTRY_NAMES.get(c, c)} ({c})"

DEFAULTS = {"in_lead": 60, "in_country": "PRT" if "PRT" in countries else countries[0], "in_segment": "Online TA",
            "in_requests": 0, "in_customer": "Transient"}
for k, v in DEFAULTS.items():
    st.session_state.setdefault(k, v)


def reset_form():  # FR-09
    for k, v in DEFAULTS.items():
        st.session_state[k] = v
    st.session_state.pop("result", None)


# ---------- Sidebar: informasi model (FR-07) ----------
with st.sidebar:
    st.header("Informasi model")
    st.write(f"**Model:** {artifact['model_name']}")
    st.write(f"**Threshold:** {artifact['threshold']:.2f}")
    m = artifact.get("metrics_test", {})
    if m:
        st.caption("Hasil pada data uji")
        st.write(f"Recall {m.get('Recall', 0):.3f} · Precision {m.get('Precision', 0):.3f}  \n"
                 f"F1 {m.get('F1', 0):.3f} · ROC-AUC {m.get('ROC-AUC', 0):.3f}")
    st.caption("Detail perbandingan model ada di halaman **Model Evaluation**.")

# ---------- Header ----------
st.title("🏨 Prediksi Pembatalan Booking Hotel")
st.write("Isi informasi reservasi di bawah ini. Aplikasi akan memperkirakan apakah reservasi tersebut "
         "**berpotensi dibatalkan**, berdasarkan pola pada data historis reservasi hotel.")
st.info("Hasil hanyalah estimasi model berdasarkan data historis, **bukan kepastian**. "
        "Jangan dipakai sebagai satu-satunya dasar untuk menolak atau memperlakukan pelanggan secara berbeda.",
        icon="ℹ️")

# ---------- Formulir (FR-01) ----------
with st.form("form_reservasi"):
    st.subheader("Informasi reservasi")
    lead_time = st.number_input("Jarak pemesanan ke kedatangan (hari)", min_value=LEAD_MIN, max_value=LEAD_MAX,
                                step=1, key="in_lead",
                                help="Jumlah hari antara tanggal pemesanan dan tanggal kedatangan.")
    country = st.selectbox("Negara asal tamu", country_options, format_func=country_fmt, key="in_country",
                           help="Negara di luar daftar dipilih lewat 'Negara lain'.")
    segment = st.selectbox("Asal pemesanan", list(SEGMENT_LABELS), format_func=SEGMENT_LABELS.get,
                           key="in_segment", help="Kanal atau pihak yang melakukan pemesanan.")
    requests = st.number_input("Jumlah permintaan khusus", min_value=REQ_MIN, max_value=REQ_MAX, step=1,
                               key="in_requests",
                               help="Contoh: tempat tidur tambahan, lantai tinggi, dan lainnya (0-5).")
    customer = st.selectbox("Tipe pelanggan", list(CUSTOMER_LABELS), format_func=CUSTOMER_LABELS.get,
                            key="in_customer")
    c1, c2 = st.columns([3, 1])
    submitted = c1.form_submit_button("Prediksi Pembatalan", type="primary")
    c2.form_submit_button("Reset", on_click=reset_form)

# ---------- Proses (FR-02, FR-03) ----------
if submitted:
    inputs = {"lead_time": int(lead_time), "country": country, "market_segment": segment,
              "total_of_special_requests": int(requests), "customer_type": customer}
    errors = validate_inputs(inputs, countries)
    if errors:
        for e in errors:
            st.error(e)
        st.session_state.pop("result", None)
    else:
        proba, label = predict(artifact, inputs)
        st.session_state["result"] = {"proba": proba, "label": label}

# ---------- Output (FR-04, FR-05, FR-06) ----------
res = st.session_state.get("result")
if res:
    proba, label, thr = res["proba"], res["label"], artifact["threshold"]
    st.divider()
    st.subheader("Hasil prediksi")
    if label == 1:
        st.warning("**Berpotensi Dibatalkan**", icon="⚠️")
    else:
        st.success("**Tidak Berpotensi Dibatalkan**", icon="✅")
    st.metric("Probabilitas pembatalan (estimasi)", f"{proba*100:.1f}%")
    st.progress(min(max(proba, 0.0), 1.0))
    st.caption(f"Model: {artifact['model_name']} · Reservasi ditandai *berpotensi dibatalkan* jika probabilitas "
               f"≥ {thr*100:.0f}%. Ambang ini dipilih agar model lebih banyak menemukan pembatalan, "
               "sehingga reservasi dengan probabilitas di atas ambang (tetapi di bawah 50%) tetap ditandai.")
    verdict = "berpotensi dibatalkan" if label == 1 else "tidak berpotensi dibatalkan"
    st.write(f"Model memperkirakan reservasi ini **{verdict}** dengan probabilitas pembatalan "
             f"**{proba*100:.0f}%**. Hasil ini merupakan estimasi berdasarkan pola pada data historis "
             "dan tidak menjamin keputusan pelanggan.")
