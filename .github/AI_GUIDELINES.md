# AI & Automation Guidelines for IODEX Expense Tracker

This file documents repository-specific guidance for automation agents and contributors who use AI tools to assist development. It is intended to make automated contributions safer, clearer, and more reviewable.

## Quick context

- Purpose: Desktop, single-user expense tracker using Tkinter. Entry point: `gui_expense_tracker.py`.
- Storage: CSV legacy mode (`storage.py`) and modern SQLite backend (`database.py`, `ExpenseDatabase`).
- Tests: pytest-based; unit tests in `test_*.py` files.

## What this file contains

- Architecture summary and conventions
- Developer workflows and commands
- Testing guidance and examples
- Integration points and optional dependencies

If you prefer a different filename or location for this guidance (for example `DEVELOPER_GUIDELINES.md` at the repo root), tell me and I will move/rename it.

---

## Core guidance (high level)

- Keep changes small and well-scoped so reviewers can quickly validate them.
- Prefer making logic changes in non-GUI modules (`storage.py`, `analysis.py`, `utils.py`) and keep `gui.py` thin and testable.
- Use the repository's test fixtures and pass `path=` or `tmp_path` to storage helpers when writing tests to avoid mutating the real data store.

## Helpful commands

```powershell
# Run app
python gui_expense_tracker.py

# Run all tests
python -m pytest -q

# Setup venv
python -m venv .venv
& ".venv/Scripts/Activate.ps1"
pip install -r requirements.txt
```

## Notes about automation

- When an AI or automation agent proposes changes, include a clear description of intent and the specific tests the change touches.
- Avoid unilateral large-scale refactors without first opening an issue and discussing with maintainers.
- Always run the project's tests locally (or in CI) and include test results in the PR description.

## Contact / review

Open an issue to discuss substantial changes or automation workflows before applying them. Maintainers will review PRs and provide feedback.
