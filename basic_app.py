"""Beginner version: display tasks, edit them, and save."""
from datetime import date
import pandas as pd
import streamlit as st
from basic_storage import COLUMNS, STATUSES, load_tasks, save_tasks

st.set_page_config(page_title="My onboarding tracker", layout="wide")
st.title("My onboarding tracker")
st.caption("Keep track of who is doing what for each customer.")
st.info("Start here: change one task's status, then click Save changes.")
if "basic_message" in st.session_state:
    st.success(st.session_state.pop("basic_message"))

# A DataFrame is a table. Load our table from the saved CSV file.
tasks = load_tasks()
editable_tasks = tasks.copy()
editable_tasks["Due date"] = editable_tasks["Due date"].map(date.fromisoformat)

# A form groups edits together until the user presses its save button.
with st.form("basic_edit"):
    edited_tasks = st.data_editor(
        editable_tasks, hide_index=True, num_rows="fixed",
        alt="Customer tasks with owners, deadlines and progress",
        column_config={
            "Due date": st.column_config.DateColumn(format="DD MMM YYYY", required=True),
            "Status": st.column_config.SelectboxColumn(options=STATUSES, required=True),
        },
    )
    save_clicked = st.form_submit_button("Save changes")

if save_clicked:
    try:
        save_tasks(edited_tasks)
        st.session_state["basic_message"] = "Your changes are saved."
        st.rerun()
    except ValueError as error:
        st.error(str(error))
    except OSError:
        st.error("Could not save the file. Check folder permissions and try again.")

# This optional form adds one task at a time.
with st.expander("Add a task"):
    with st.form("basic_add", clear_on_submit=True):
        customer = st.text_input("Customer", key="basic_customer")
        task = st.text_input("Task", key="basic_task")
        owner = st.text_input("Owner", key="basic_owner")
        due_date = st.date_input("Due date", date.today(), key="basic_due")
        add_clicked = st.form_submit_button("Add task")
    if add_clicked:
        new_task = pd.DataFrame(
            [[customer, task, owner, due_date.isoformat(), "Not started"]],
            columns=COLUMNS,
        )
        try:
            updated_tasks = pd.concat([load_tasks(), new_task], ignore_index=True)
            save_tasks(updated_tasks)
            st.session_state["basic_message"] = "Your new task is saved."
            st.rerun()
        except ValueError as error:
            st.error(str(error))
        except OSError:
            st.error("Could not save the task. Check folder permissions and try again.")
