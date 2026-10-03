import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import basic_storage

class BasicTrackerTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.path = Path(self.directory.name) / "basic_tasks.csv"
        self.patch = patch.object(basic_storage, "DATA_FILE", self.path)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.directory.cleanup()

    def test_saved_edits_survive_reload(self):
        tasks = basic_storage.load_tasks()
        self.assertEqual(len(tasks), 3)
        tasks.loc[0, "Status"] = "Done"
        basic_storage.save_tasks(tasks)
        self.assertEqual(basic_storage.load_tasks().iloc[0]["Status"], "Done")

    def test_invalid_edits_preserve_saved_file(self):
        tasks = basic_storage.load_tasks()
        original = self.path.read_bytes()
        for column, value in [("Owner", "  "), ("Due date", "not-a-date"), ("Status", "Unknown")]:
            invalid = tasks.copy()
            invalid.loc[0, column] = value
            with self.subTest(column=column):
                with self.assertRaises(ValueError):
                    basic_storage.save_tasks(invalid)
                self.assertEqual(self.path.read_bytes(), original)

    def test_native_dates_from_editor(self):
        tasks = basic_storage.load_tasks()
        tasks["Due date"] = [date(2026, 10, 4)] * len(tasks)
        basic_storage.save_tasks(tasks)
        self.assertEqual(basic_storage.load_tasks().iloc[0]["Due date"], "2026-10-04")

    def test_add_task_through_form(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "basic_app.py")).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(len(app.dataframe[0].value), 3)
        app.text_input(key="basic_customer").set_value("Acme Studio")
        app.text_input(key="basic_task").set_value("Send a welcome email")
        app.text_input(key="basic_owner").set_value("Abhinandan")
        next(b for b in app.button if b.label == "Add task").click().run()
        self.assertFalse(app.exception)
        saved = basic_storage.load_tasks()
        self.assertEqual(len(saved), 4)
        self.assertEqual(saved.iloc[-1]["Task"], "Send a welcome email")
        next(b for b in app.button if b.label == "Add task").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(app.error)
        self.assertEqual(len(basic_storage.load_tasks()), 4)
