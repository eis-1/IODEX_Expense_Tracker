# IODEX — Super Duper Expense Tracker

A lightweight desktop expense tracker built with Python and Tkinter. Designed for personal use, the app lets you quickly add expenses, view them in a table, and analyze totals by category. This README documents the project layout, how it works, how to run it, and recommended ideas for future upgrades and optimizations.

## Table of Contents

- Project overview
- Project structure
- How it works (quick walkthrough)
- Data format
- Installation
- Usage
- Development & testing
- Upgrade / Optimize / Add features (Roadmap)
- Contributing
- License & contact

## Project overview

IODEX is a single-user, local GUI application to track personal expenses. It stores records in a simple text file (`expenses.txt`) and uses common Python libraries for plotting and data handling.

## Project structure

- `gui_expense_tracker.py` — Main GUI application and program entry point.
- `expenses.txt` — Plain-text persistent storage for expense records (one record per line).
- `requirements.txt` — Python dependencies (if any third-party packages are used).

If you add more modules, keep the top-level layout shallow and group helpers in a `src/` or `io/` folder.

## How it works (quick walkthrough)

- On start the GUI initializes and ensures `expenses.txt` exists.
- Adding an expense appends a new line to `expenses.txt` in the format described below.
- Viewing loads `expenses.txt` into a table widget (simple parsing, no DB required).
- Analysis loads the records into a pandas DataFrame (if available) and builds a category summary and bar chart using matplotlib/seaborn.
- Reset/clear deletes or truncates `expenses.txt` (confirm before destructive actions).

## Data format

Current storage is a comma-separated plain text file. Each line represents one expense:

Category,Amount,Description

Example:

Food,12.50,Lunch at cafe
Transport,2.75,Bus fare

Notes:
- Amount should be a numeric value (float). Use a period for decimals.
- Commas in descriptions are not escaped by the current parser. Consider switching to CSV with quoting or to SQLite for robust parsing.

## Installation

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Unix / macOS
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Notes: Tkinter is part of the Python standard library on most installations. If your platform lacks it, install the system package (e.g., `sudo apt install python3-tk` on Debian/Ubuntu).

## Usage

Run the application from the repository root:

```bash
python gui_expense_tracker.py
```

Behavior:
- The app creates `expenses.txt` when first run if it does not exist.
- Use the GUI fields to add category, amount and an optional description.
- Use the View/Analyze buttons to inspect your data and totals.

## Development & testing

- Recommended: add a `tests/` folder and write unit tests for parsing, persistence, and any new business logic.
- Use `pytest` for quick test runs: `pip install pytest` and `pytest -q`.
- Keep GUI logic separated from data logic: create a small module (e.g., `storage.py`) with functions `load_expenses()`, `save_expense()`, `clear_expenses()` and test those directly.

## Upgrade / Optimize / Add features (Roadmap)

Short-term improvements (low effort, high value):
- Move storage from free-form text to CSV using Python's `csv` module (supports safe quoting/commas).
- Refactor to separate modules: `gui.py`, `storage.py`, `analysis.py` to keep code testable and maintainable.
- Add input validation and better error messages (e.g., highlight the amount field when invalid).

Medium-term enhancements:
- Replace text storage with SQLite (`sqlite3`) for reliability, queries, and atomic writes.
- Add import/export (CSV, JSON) and backup functionality.
- Persist UI settings (window size, last directory) using `configparser` or simple JSON.
- Add logging (use the `logging` module) for easier debugging.

Long-term / value-add features:
- Multi-currency support and automatic exchange rates (careful with network calls).
- Authentication / multi-user profiles (if moving to a shared environment or server).
- Convert to a web app (Flask/FastAPI + a small frontend) for remote access or multi-device sync.
- Build installers for Windows/macOS (PyInstaller, briefcase) for easier distribution.

Performance & safety notes:
- When moving to larger datasets prefer SQLite and use indexes for fast aggregation.
- Avoid executing or evaluating user-provided strings; sanitize inputs.

## Suggested development tasks to get started

1. Add `storage.py` with functions:
   - `load_expenses(path) -> list[tuple]`
   - `append_expense(path, category, amount, description)`
   - `clear_expenses(path)`
2. Update `gui_expense_tracker.py` to import and call these functions instead of inlined file operations.
3. Add unit tests for `storage.py` and parsing edge cases (commas in description, negative amounts, malformed lines).

## Contributing

- Fork the repo, create a feature branch, and open a pull request.
- Keep changes small and focused; include tests for new logic.

## License

Add a `LICENSE` file if you want to define how others may use your code. If you prefer permissive reuse, consider the MIT license.

## Contact

If you'd like help implementing any of the roadmap items above, open an issue describing what you want to change and include relevant screenshots or logs.

---