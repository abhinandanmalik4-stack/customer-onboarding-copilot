# Stage 1: Start onboarding a customer

The earlier working prototype is the baseline. This stage adds customer creation to it.
Git preserves the baseline and records this real change as a new commit.

## What to try
1. Launch Start.cmd and open the Tracker tab.
2. Expand Start onboarding a customer.
3. Enter Acme Studio, Abhinandan and 2026-10-04.
4. Click Create onboarding plan.
5. Find the six new tasks. Their dates run from October 4 through October 14.
6. Change individual owners and dates in Edit the full tracker, then click Save tracker.
7. Restart the app: saved records should remain.
8. Try adding ACME STUDIO again: validation prevents a duplicate.

These are calendar-day demo defaults, not a promised onboarding duration.

## Vocabulary
A customer is the business purchasing the SaaS product.
An owner is the person accountable for a task.
A milestone is a checkpoint such as testing or go-live.
A dependency is another task that must be completed first.
Persistence means data survives a program restart.
Validation means checking inputs before accepting them.
A DataFrame is Pandas' table of rows and columns.
A UUID is a randomly generated identifier used to distinguish tasks.
A function takes inputs, performs a defined operation and returns a result.

## Follow the request through the code
1. app.py renders a Streamlit form with name, owner and kickoff date.
2. The form batches edits until Create onboarding plan is pressed.
3. load_tasks reads the latest saved tracker.
4. create_customer in core.py receives that table and the three form values.
5. It normalizes spaces and checks required values and duplicate customer names.
6. A list defines the six workflow stages and their date offsets.
7. A loop generates one record per stage. timedelta adds calendar days.
8. Each new record gets a UUID. Each stage after kickoff points to the previous task ID.
9. pd.concat combines existing records and new records into a new table.
10. validate_tasks checks IDs, status, dates and dependencies.
11. The function returns the table. It does not write to disk.
12. save_csv in integrations.py writes a temporary CSV, then replaces the saved file.
13. st.rerun reloads the script so the dashboard reflects the saved data.
14. A session-state message survives that rerun and confirms the save.

## Why separate these responsibilities?
app.py handles what the user sees and clicks.
core.py handles rules independently of Streamlit.
integrations.py handles storage and external services.
This separation lets tests exercise business rules without opening a browser.

## Interview questions and explanations
Why start with a tracker before AI?
The tracker establishes reliable customer records and task ownership that later features use.

Why a form?
It submits related inputs together instead of creating records on every text edit.

Why normalize names?
Capitalization and repeated spaces should not create duplicate customer records in this prototype.
A production system should use a separate customer ID and support legal entities with identical names.

Why task IDs rather than task names?
Every customer has a Setup task. IDs keep dependency references unambiguous.

Why not immediately save inside create_customer?
Keeping creation separate from storage makes the rules easier to test and reuse.

Why all tasks start as Not started?
Creating a plan does not prove that any work has been completed.

Why does every task initially have the same owner?
The initial owner is the coordinator. The user can assign specific task owners after creation.

Why save through a temporary file?
It reduces the chance of leaving a partially written CSV if writing fails before replacement.
It does not solve concurrent editing; a multi-user system needs database transactions.

What are the limitations?
Six fixed stages, calendar-day default dates, single coordinator initially, CSV storage,
no authentication, and duplicate detection based on names. These are prototype choices.

How was this stage tested?
Tests check six-task creation, date arithmetic across months/years, dependency links,
unchanged original records, blank inputs, duplicate names, persisted form submission,
and rejection without changing the saved file.

## Git basics
Working files: the code you are editing.
Staging: selecting changes for the next commit.
Commit: a saved checkpoint with a message describing the change.
The repositories are local; a commit does not publish anything to GitHub.

Useful commands from this repository:
git status
git log --oneline
git show --stat HEAD

Each future working stage should include its code, relevant tests, explanation and commit.

## Next lesson
Deadline and dependency rules: explain why a task can be blocked without being overdue.
