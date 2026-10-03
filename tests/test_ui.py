import tempfile, unittest
from pathlib import Path
from unittest.mock import patch
from streamlit.testing.v1 import AppTest
import core
from integrations import save_csv

class UITests(unittest.TestCase):
    def test_load_answer_and_extract(self):
        with tempfile.TemporaryDirectory() as tmp:
            data=Path(tmp)
            save_csv(core.seed_tasks(),data/"tasks.csv")
            with patch.object(core,"DATA",data),patch.object(core,"TASKS",data/"tasks.csv"):
                app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/"app.py")).run(timeout=30)
                self.assertFalse(app.exception)
                self.assertEqual(app.metric[0].value,"8")
                app.text_input(key="question").set_value("How do I invite users?").run()
                app.button(key="answer").click().run()
                self.assertFalse(app.exception)
                app.button(key="extract").click().run()
                self.assertFalse(app.exception)
                self.assertEqual(len(app.session_state["actions"]),2)

