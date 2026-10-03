# Lesson 1: Your first customer tracker

Launch Start.cmd. Study only basic_app.py and basic_storage.py for this lesson.
The larger prototype is available separately through Start-Advanced.cmd.

## What is this?
Imagine Acme Studio bought an online software product.
You need to meet the customer, set up their account and teach them how to use it.
Each table row describes one piece of work.

Customer: the business receiving help.
Task: the work that needs to happen.
Owner: the person responsible for doing it.
Due date: when the work should be finished.
Status: Not started, In progress or Done.

## What we built
- A table with three fictional starter tasks.
- A way to edit and save the table.
- A form to add one task.
- Checks that reject blank details and invalid dates.
- A local file that remembers the work after the app closes.

## The two files
basic_app.py creates the screen, buttons and forms.
basic_storage.py reads and saves the task table.

## Vocabulary
Python: the programming language used to write the instructions.
Streamlit: a library that creates the screen and buttons.
Library: reusable code that helps with common tasks.
Pandas: a library for working with tables.
DataFrame: Pandas' name for a table of rows and columns.
CSV: a text file that stores a table.
Function: a named piece of code that performs a particular job.
Validation: checking information before accepting it.

## When the app opens
1. load_tasks() checks for data/basic_tasks.csv.
2. If missing, it creates three starter tasks.
3. Pandas reads the CSV into a DataFrame.
4. Streamlit displays that table.

## When you click Save changes
1. Streamlit collects the edited table.
2. save_tasks() calls check_tasks().
3. check_tasks() checks required values, statuses and dates.
4. Invalid data produces an error; the previous file remains unchanged.
5. Valid data is written to a temporary CSV.
6. The temporary file replaces the saved CSV.
7. Streamlit reruns the screen and displays the saved version.

A temporary file reduces the chance of a half-written main file.
It does not prevent conflicting edits by multiple people.

## Read basic_app.py in order
Imports bring in library tools.
Title and instructions tell the user what to do.
load_tasks() gets the existing table.
st.data_editor() displays an editable table.
st.form_submit_button() provides a button.
save_tasks() writes changes after a click.
The Add a task form combines a new row with the existing table.
st.session_state remembers the success message during the screen refresh.

## Interview questions
What does this version do?
It tracks customer onboarding tasks, owners, deadlines and progress.

Why Streamlit?
It provides a Python interface without needing a separate web frontend.

Where is the data?
In a local CSV. Pandas loads it as a DataFrame and saves changes back.

Why validation?
Missing owners and invalid dates make a tracker unreliable.

Does this lesson use AI?
No. The basic tracker is the foundation for later features.

What are the limitations?
Single-user local storage, no login, reminders, dependencies or AI.
It allows duplicate task rows. IDs and duplicate rules can come later.

Why two files?
The screen and storage have separate responsibilities, making them easier to understand and test.

## Five-minute exercise
1. Open Start.cmd.
2. Set Hold the kickoff meeting to Done.
3. Click Save changes.
4. Close and reopen the app; confirm it is still Done.
5. Add: Acme Studio / Send a welcome email / your name.
6. Explain aloud: input, check, save, display.

## Git
A commit is a saved checkpoint of the source code.
This beginner version has its own commit in the existing local repository.
Changing task records are ignored by Git because they are working data.
No files have been published to GitHub.

Next: explain these two small files line by line, then add an overdue indicator.
