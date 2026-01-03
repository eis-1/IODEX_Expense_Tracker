# AI Agent Instructions for IODEX Expense Tracker

This document gives focused, actionable guidance so an AI coding agent can be immediately productive in this repository.

Quick context

- Purpose: Desktop, single-user expense tracker using Tkinter. Entry point: `gui_expense_tracker.py`.
- Primary storage: CSV-style plain text file `expenses.txt` managed by `storage.py`.
- Tests: pytest-based, files named `test_*.py`.

What to look at first (big picture)

- `gui.py` — `ExpenseTrackerGUI` contains UI flows and is the place to add UI controls or navigation.
- `storage.py` — read/write/clear/delete helpers. Functions accept an optional `path` argument for testability.
- `analysis.py` — aggregation and plotting helpers. Static charts use `matplotlib`/`seaborn`; optional interactive charting via `plotly` and `pywebview`.
- `config.py` — config persistence to `config.json` (timestamp preferences).
- `utils.py` — timestamp formatting helpers (useful for unit tests and preview logic).

Key patterns and conventions

- Storage functions take an explicit `path` parameter. When changing or testing storage behavior, prefer passing a temp path instead of touching `expenses.txt`.
- Use Python's `csv` module for robust CSV handling (descriptions may include commas/quotes/newlines).
- Timestamps are recorded as ISO-8601 UTC strings; GUI converts according to preferences (local/UTC/custom) using `utils.format_iso_timestamp()`.
- GUI entry/exit: call `self.main_menu()` to return to the main menu. Screens with Back buttons implement `command=self.main_menu`.
- Tests cover non-GUI logic; GUI changes should be accompanied by testable helper functions (see `ExpenseTrackerGUI.compute_preview_text()` as an example).

Developer workflows (commands)

- Run app (from repo root):
  ```powershell
  python gui_expense_tracker.py
  ```
- Run tests:
  ```powershell
  python -m pytest -q
  ```
- Create venv and install deps:
  ```powershell
  python -m venv .venv
  .venv\Scripts\activate
  pip install -r requirements.txt
  ```

Integration points & optional dependencies

- `pandas`, `matplotlib`, `seaborn` — required for analysis and plotting.
- `plotly` + `pywebview` — optional: enables interactive charts; guard code checks availability before use.
- `Pillow` — optional image background support.

Where to make common changes

- Add screens, buttons, or navigation: modify `gui.py` (`ExpenseTrackerGUI`). Keep business logic in `storage.py` / `analysis.py`.
- Storage schema changes: update `storage.py` and adjust tests in `test_storage.py`.
- Charting changes: `analysis.py` and export via `_export_chart()` in `gui.py`.

Examples (concrete pointers)

- Return to main menu: `gui.py` contains `tk.Button(..., text="🔙 Back", command=self.main_menu)` in `view_expenses()`, `analyze_expenses()`, and `open_preferences()`.
- Preview helper used in tests: `ExpenseTrackerGUI.compute_preview_text(sample_iso, mode, custom_fmt, show_rel, tz_name)`.
- Delete behavior: `_delete_selected()` in `gui.py` calls `storage.delete_expense(...)` matching by `(category, amount, description, timestamp)`.

Testing guidance for AI edits

- Prefer adding unit tests for `storage.py`, `analysis.py`, or `utils.py`. Tests live as `test_*.py` files.
- Use temporary files via `tmp_path` pytest fixture and pass `path=` to storage functions.
- Keep GUI changes minimal in logic; extract non-GUI logic to helpers so tests can validate behavior without launching Tk.

When updating this file

- If `.github/copilot-instructions.md` already exists, merge by preserving any project-specific rules and adding missing commands listed above.

If anything in this guidance is unclear or you want examples of unit tests to add, tell me which area (storage, analysis, utils, GUI) and I will generate targeted tests or code changes.
