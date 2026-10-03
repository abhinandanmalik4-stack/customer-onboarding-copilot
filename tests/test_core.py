import unittest
from unittest.mock import patch
from datetime import date
from core import *

class CoreTests(unittest.TestCase):
    def test_flags(self):
        df=seed_tasks(date(2026,10,3)).head(3).copy()
        df.loc[0,["status","due_date"]]=["Done","2026-10-01"]
        df.loc[1,["status","due_date"]]=["In progress","2026-10-03"]
        df.loc[2,["status","due_date"]]=["Not started","2026-10-02"]
        out=flags(df,date(2026,10,3))
        self.assertFalse(out.iloc[0].overdue)
        self.assertFalse(out.iloc[1].overdue or out.iloc[1].blocked)
        self.assertTrue(out.iloc[2].overdue and out.iloc[2].blocked)
    def test_cycle(self):
        df=seed_tasks().head(2).copy()
        df.loc[0,"dependency"]=df.iloc[1].id
        with self.assertRaises(ValueError): validate_tasks(df)
    def test_invalid_dependency(self):
        df=seed_tasks()
        df.loc[6,"dependency"]=df.iloc[0].id
        with self.assertRaises(ValueError): validate_tasks(df)
    def test_faq(self):
        self.assertEqual(answer("How do I invite users?")["sources"],["F1"])
        self.assertTrue(answer("Can you guarantee security for users?")["escalate"])
        self.assertTrue(answer("What is your refund policy?")["escalate"])
    def test_extraction_and_dedupe(self):
        actions=extract_actions("Asha: Test access | due 2026-10-07\nWe discussed launch.")
        self.assertEqual(len(actions),1)
        first=add_actions(seed_tasks(),"Demo Customer 01",actions)
        self.assertEqual(len(add_actions(first,"Demo Customer 01",actions)),len(first))
        actions.loc[0,"due_date"]=""
        with self.assertRaises(ValueError): add_actions(first,"Demo Customer 01",actions)
    def test_claude_source_guard(self):
        with patch("core.claude_json",return_value={"answer":"Invented","sources":["INVALID"],"escalate":False}):
            self.assertTrue(answer("Question",True)["escalate"])
    def test_sample_customer_count(self):
        self.assertEqual(seed_tasks().customer.nunique(),8)
        self.assertEqual(len(seed_tasks()),48)
