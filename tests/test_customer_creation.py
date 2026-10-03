import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

import pandas as pd
from streamlit.testing.v1 import AppTest
import core
from integrations import save_csv


class CustomerCreationTests(unittest.TestCase):
    def test_plan_dates_chain_and_original_records(self):
        original = core.seed_tasks(date(2026, 10, 4))
        result = core.create_customer(original, " Acme   Studio ", " Abhinandan ", date(2026, 10, 4))
        new = result[result.customer.eq("Acme Studio")].reset_index(drop=True)
        self.assertEqual(len(result), 54)
        pd.testing.assert_frame_equal(result.iloc[:48], original)
        self.assertEqual(new.task.tolist(), ["Kickoff", "Requirements", "Setup", "Testing", "Training", "Go-live"])
        self.assertEqual(new.due_date.tolist(), ["2026-10-04", "2026-10-06", "2026-10-08", "2026-10-10", "2026-10-12", "2026-10-14"])
        self.assertTrue(new.owner.eq("Abhinandan").all())
        self.assertTrue(new.status.eq("Not started").all())
        self.assertEqual(new.dependency.tolist(), [""] + new.id.tolist()[:-1])
        self.assertTrue(result.id.is_unique)
        self.assertEqual(len(original), 48)

    def test_duplicate_names_ignore_case_and_spaces(self):
        first = core.create_customer(core.seed_tasks(), "Acme Studio", "Asha", date.today())
        with self.assertRaisesRegex(ValueError, "already exists"):
            core.create_customer(first, " ACME   studio ", "Rohan", date.today())

    def test_required_inputs(self):
        for customer, owner in [("  ", "Asha"), ("Acme", "  ")]:
            with self.subTest(customer=customer, owner=owner):
                with self.assertRaises(ValueError):
                    core.create_customer(core.seed_tasks(), customer, owner, date.today())

    def test_month_boundary(self):
        result = core.create_customer(core.seed_tasks(), "Acme", "Asha", date(2026, 12, 28))
        new = result[result.customer.eq("Acme")]
        self.assertEqual(new.iloc[-1].due_date, "2027-01-07")

    def test_form_persists_and_duplicate_does_not_change_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            data = Path(tmp)
            path = data / "tasks.csv"
            save_csv(core.seed_tasks(), path)
            with patch.object(core, "DATA", data), patch.object(core, "TASKS", path):
                app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "app.py")).run(timeout=30)
                app.text_input(key="new_customer_name").set_value("Acme Studio")
                app.text_input(key="new_customer_owner").set_value("Abhinandan")
                next(b for b in app.button if b.label == "Create onboarding plan").click().run()
                self.assertFalse(app.exception)
                self.assertEqual(app.metric[0].value, "9")
                persisted = pd.read_csv(path)
                self.assertEqual(len(persisted), 54)
                before = path.read_bytes()
                next(b for b in app.button if b.label == "Create onboarding plan").click().run()
                self.assertFalse(app.exception)
                self.assertIn("already exists", app.error[0].value)
                self.assertEqual(path.read_bytes(), before)
