"""Read and save the beginner tracker's table."""
from datetime import date, timedelta
from pathlib import Path
import pandas as pd

DATA_FILE = Path(__file__).resolve().parent / "data" / "basic_tasks.csv"
COLUMNS = ["Customer", "Task", "Owner", "Due date", "Status"]
STATUSES = ["Not started", "In progress", "Done"]

def check_tasks(table):
    """Reject missing values or invalid dates before saving."""
    if list(table.columns) != COLUMNS:
        raise ValueError("The tracker needs Customer, Task, Owner, Due date and Status columns.")
    clean = table.fillna("").astype(str).copy()
    for column in COLUMNS:
        clean[column] = clean[column].str.strip()
        if clean[column].eq("").any():
            raise ValueError(f"Please fill in every {column} value.")
    if not clean["Status"].isin(STATUSES).all():
        raise ValueError("Choose Not started, In progress or Done.")
    for value in clean["Due date"]:
        try:
            date.fromisoformat(value)
        except ValueError:
            raise ValueError("Choose a valid due date.") from None
    return clean

def save_tasks(table):
    """Check the table, write a temporary file, then replace the saved file."""
    clean = check_tasks(table)
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    temporary_file = DATA_FILE.with_suffix(".tmp")
    clean.to_csv(temporary_file, index=False)
    temporary_file.replace(DATA_FILE)

def load_tasks():
    """Read saved work, or create three fictional tasks on the first run."""
    if not DATA_FILE.exists():
        today = date.today()
        starter_tasks = [
            ["Acme Studio", "Hold the kickoff meeting", "Abhinandan", today.isoformat(), "Not started"],
            ["Acme Studio", "Set up the account", "Abhinandan", (today + timedelta(days=2)).isoformat(), "Not started"],
            ["Acme Studio", "Train the customer", "Abhinandan", (today + timedelta(days=4)).isoformat(), "Not started"],
        ]
        save_tasks(pd.DataFrame(starter_tasks, columns=COLUMNS))
    return check_tasks(pd.read_csv(DATA_FILE, dtype=str, keep_default_na=False))
