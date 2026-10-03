# Understand and demonstrate this project
Explain the problem: onboarding tasks spread across teams can miss deadlines and block launches.
Explain the records: stable task ID, customer, owner, date, status and prerequisite.
Explain the flags: a task due today is not overdue; completed tasks are never flagged.
Explain validation: dependencies cannot point to another customer or form a cycle.
Explain the assistant: match an FAQ or ask Claude using FAQ context; unsupported questions go to a human.
Explain note extraction: structured local parsing or optional AI extraction, followed by mandatory review.
Explain persistence: CSV keeps state across app restarts; production needs database transactions.

Five-minute demo:
1. Show eight customers and their task status.
2. Change a due date and complete a prerequisite; watch flags change.
3. Ask How do I invite users? Show source F1.
4. Ask about a refund. Show the human queue.
5. Extract two call-note actions, review them and save.
6. Download the tracker for Google Sheets.

Practice before the interview:
Day 1: run app and read core.py.
Day 2: predict flags and test dependency errors.
Day 3: explain retrieval, escalation and reviewed actions without reading notes.
Do not describe this as a past production deployment. Explain the newly built simulation honestly.
