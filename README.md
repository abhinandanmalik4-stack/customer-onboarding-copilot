# Customer onboarding and success copilot

## Beginner version: start here
Double-click Start.cmd for a simple tracker with one table, Save changes, and Add a task.
Read [your first lesson](docs/START_HERE.md). Study only basic_app.py and basic_storage.py initially.
This version uses separate local data in data/basic_tasks.csv.
The full prototype is available through Start-Advanced.cmd.

A runnable simulated SaaS onboarding program for eight customers.

## Run
Double-click Start.cmd for the beginner tracker or Start-Advanced.cmd for the full prototype. Both use the installed parent environment or your local .venv.
To make this repository standalone elsewhere: run Setup.cmd (requires Python 3.12), then Start.cmd.
From an activated environment: python -m streamlit run basic_app.py --server.port 8501.
For the full prototype, replace basic_app.py with app.py.
Tests: python -m unittest discover -s tests -v.

## Features
48 seed tasks spanning kickoff, requirements, setup, testing, training and go-live.
Editable owners, due dates, status and dependencies; cycle and reference validation.
Overdue means unfinished and due before the selected date; blocked means its direct prerequisite is unfinished.
FAQ retrieval with reference IDs and a persistent human escalation queue.
Call-note action extraction with preview, required-field checks and exact duplicate prevention.
Local CSV persistence and download; optional Google Sheets export to a NEW worksheet.
The fixture is generated on first launch relative to today's date. Existing tasks are never reset automatically.

## Optional Claude
Set ANTHROPIC_API_KEY and ANTHROPIC_MODEL in your terminal, then start the app there.
Example PowerShell: $env:ANTHROPIC_API_KEY = "your-key"
Use a model available to your account. Never commit keys.
Select Claude API and explicitly invoke an assistant action.
API mode sends entered notes/questions and FAQ context to Claude and may incur charges.
No Claude calls are made in local mode.
The assistant validates JSON and reference IDs, but valid IDs alone cannot prove every claim is supported.

## Optional Google Sheets
Enable Sheets and Drive APIs, create a service account, and share a destination spreadsheet
with its email as Editor. Set GOOGLE_SERVICE_ACCOUNT_FILE to the credential JSON path and
GOOGLE_SHEET_ID to the spreadsheet ID. Choose a new worksheet name and click Upload.
Credentials are not included. CSV import works without them.
No existing worksheet is overwritten.

## Structure
app.py: interface; core.py: business rules; integrations.py: API, Sheets and CSV helpers;
tests/: business and UI tests; data/: local state; docs/: demonstration notes.

## Limitations
Single-user CSV persistence; simultaneous writers need database transactions.
Local FAQ lookup is a conservative keyword baseline, not an LLM.
Local notes use Owner: task | due YYYY-MM-DD. Claude supports free-form notes.
This is a portfolio simulation, not an integration with Publive's actual product.
Live Claude and Sheets need credentials and independent verification.
Do not claim measured time savings before measuring them.

References:
https://docs.streamlit.io/develop/api-reference
https://platform.claude.com/docs/en/api/python/messages/create
https://docs.gspread.org/en/latest/oauth2.html

## Guided build
Start with [Stage 1: customer creation and tracking](docs/STAGE_01_CUSTOMER_TRACKER.md).
The Tracker tab now creates a six-task plan for a new customer with an initial owner and kickoff date.

## Open in VS Code
Open Onboarding-Copilot.code-workspace, then use Terminal > Run Task > Run beginner tracker.
Read [the complete Hinglish beginner guide](docs/BEGINNER_GUIDE_HINGLISH.md) for the purpose, code flow, interview explanations and future roadmap.

