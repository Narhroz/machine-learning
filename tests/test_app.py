"""Unit test & smoke test otomatis untuk aplikasi StayCheck."""
import math
import unittest
from streamlit.testing.v1 import AppTest

from utils import (
    load_artifact,
    known_countries,
    validate_inputs,
    predict,
    explain_local_drivers,
    threshold_zone,
    OTHER_COUNTRY,
    LEAD_MIN,
    LEAD_MAX,
    REQ_MIN,
    REQ_MAX,
    BASE,
)


class TestUtils(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.artifact = load_artifact()
        cls.countries = known_countries(cls.artifact)

    def test_artifact_structure(self):
        self.assertIsNotNone(self.artifact)
        for key in ("pipeline", "model_name", "threshold", "features"):
            self.assertIn(key, self.artifact)

    def test_validate_inputs_valid_and_other_country(self):
        valid = {
            "lead_time": 60,
            "country": self.countries[0],
            "market_segment": "Online TA",
            "total_of_special_requests": 1,
            "customer_type": "Transient",
        }
        self.assertEqual(validate_inputs(valid, self.countries), [])
        valid_other = dict(valid, country=OTHER_COUNTRY)
        self.assertEqual(validate_inputs(valid_other, self.countries), [])

    def test_validate_inputs_rejects_invalid(self):
        bad = {
            "lead_time": LEAD_MAX + 10,
            "country": "XXX",
            "market_segment": "Undefined",
            "total_of_special_requests": REQ_MAX + 1,
            "customer_type": "Unknown",
        }
        errs = validate_inputs(bad, self.countries)
        self.assertEqual(len(errs), 5)

        nan_case = {
            "lead_time": float("nan"),
            "country": self.countries[0],
            "market_segment": "Direct",
            "total_of_special_requests": True,
            "customer_type": "Transient",
        }
        self.assertGreaterEqual(len(validate_inputs(nan_case, self.countries)), 2)

    def test_predict_and_explain_drivers(self):
        inp = {
            "lead_time": 200,
            "country": "PRT",
            "market_segment": "Online TA",
            "total_of_special_requests": 0,
            "customer_type": "Transient",
        }
        proba, label = predict(self.artifact, inp)
        self.assertTrue(0.0 <= proba <= 1.0)
        self.assertIn(label, (0, 1))

        drivers = explain_local_drivers(self.artifact, inp)
        self.assertEqual(len(drivers), len(self.artifact["features"]))
        self.assertGreaterEqual(abs(drivers[0]["delta_pp"]), abs(drivers[-1]["delta_pp"]))

    def test_threshold_zone(self):
        thr = 0.30
        self.assertEqual(threshold_zone(0.31, thr)[0], "near")
        self.assertEqual(threshold_zone(0.60, thr)[0], "high")
        self.assertEqual(threshold_zone(0.05, thr)[0], "low")


class TestStreamlitPages(unittest.TestCase):
    def test_home_prediction_history_and_reset(self):
        at = AppTest.from_file(str(BASE / "app.py")).run(timeout=30)
        self.assertEqual(len(at.exception), 0)

        # Klik tombol Prediksi pembatalan
        pred_btn = [b for b in at.button if b.label == "Prediksi pembatalan"][0]
        pred_btn.click().run(timeout=30)
        self.assertEqual(len(at.exception), 0)
        self.assertIn("result", at.session_state)
        self.assertEqual(len(at.session_state["history"]), 1)

        # Klik Atur ulang
        reset_btn = [b for b in at.button if b.label == "Atur ulang"][0]
        reset_btn.click().run(timeout=30)
        self.assertNotIn("result", at.session_state)

    def test_evaluation_and_about_pages(self):
        for page in ("pages/1_Model_Evaluation.py", "pages/2_About_Project.py"):
            at = AppTest.from_file(str(BASE / page)).run(timeout=30)
            self.assertEqual(len(at.exception), 0)


if __name__ == "__main__":
    unittest.main()
