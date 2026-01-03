IODEX — Desktop Expense Tracker

A compact, single-user desktop expense tracker written in Python with a Tkinter GUI. The app records expense entries to a local CSV-style text file, displays stored records, and provides simple category-based analysis (charts). This repository contains the application source, unit tests, and runtime configuration.

Status: stable for local use — suitable for demos, coursework, and small personal budgets.

Table of Contents

- Project overview
- Key features
- Quick start
- File map (what's in this repo)
- Usage
- Testing
- Development notes
- Contributing
- License & contact

## Project overview

IODEX is designed as a small, easy-to-run personal expense tracker. It focuses on clarity, testability, and a clean separation between storage, analysis, and presentation layers.

Goals:

- Simple expense recording (category, amount, description, timestamp).
- Human-readable, robust storage (`expenses.txt` using CSV quoting).
- Basic analysis (category totals, bar chart).
- Well-tested non-GUI logic with pytest.

## Key features

- Add expense entries with category, numeric amount, and description.
- Robust CSV storage that handles commas, quotes, and newlines in descriptions.
- View all expenses in a table with a running total.
- Category-wise aggregation and embedded bar chart visualization.
- Reset/clear stored expenses from the GUI.
- Preferences persisted in `config.py` / `config.json` (timestamp format, timezone display).
- Comprehensive unit tests for storage, utils, and analysis modules.

## Quick start (Windows)

1. Clone the repository and change directory:

```powershell
cd "d:/siam/Object-oriented final project"
```

2. (Recommended) Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the GUI:

```powershell
python gui_expense_tracker.py
```

Notes:

- `expenses.txt` is created automatically when the first expense is saved.
- Optional background image: place `photo1.jpg` next to `gui_expense_tracker.py`.

## File map (what's in this repo)

- `gui_expense_tracker.py` — application entry point / launcher
- `gui.py` — Tkinter GUI implementation (`ExpenseTrackerGUI` and dialogs)
- `storage.py` — persistence layer (append, load, clear, totals). Use `path` parameter to point at alternate files for testing.
- `analysis.py` — aggregation and chart creation helpers
- `database.py` — (if present) optional DB helpers or migration utilities
- `import_export.py` — CSV/JSON import-export helpers
- `config.py` — reads/writes `config.json` for UI preferences
- `utils.py` — helper utilities (time formatting, validation)
- `backup.py` — optional backup utilities
- `expenses.txt` — runtime CSV-style data file (not checked into VCS with personal data)
- `requirements.txt` — Python dependencies
- `test_*.py` — pytest test suite for storage/analysis/utils/gui behaviors

## Usage (summary)

- Add an expense: open the app, choose `Add Expense`, fill category & amount, optional description, click OK.
- View expenses: `View All Expenses` — table view with totals.
- Analyze: `Analyze Expenses` — category bar chart (matplotlib/seaborn). If `plotly`+`pywebview` are installed, interactive charts may open in a native window or browser.
- Reset: `Reset Expenses` clears `expenses.txt` after confirmation.

## Tests

IODEX — Desktop Expense Tracker

Make this repository stand out on GitHub: the README below is written to be clear, emphatic, and ready-to-copy into the repository home page. It includes exact commands, tests, and where to find the Back button that returns to the main menu.

Badges (optional)

- CI: Add a GitHub Actions badge when you enable CI.
- PyPI / Downloads: Add when publishing.

## Overview

IODEX is a compact, single-user desktop expense tracker written in Python with a Tkinter GUI. It stores expenses in a robust CSV-style text file (`expenses.txt`) and provides a simple category analysis chart. The project emphasizes:

- Simple, local persistence (human-readable CSV quoting)
- Clear separation: `storage.py`, `analysis.py`, `gui.py`
- Test coverage of non-GUI logic with `pytest`

## Quick highlights

- Add/View/Delete expenses
- Category aggregation and charting (static + optional interactive)
- Preferences (timestamp display) with persistent config
- Unit tests: run with `pytest`

## Install and run (Windows example)

1. Open a terminal and change to the project folder:

```powershell
cd "d:/siam/Object-oriented final project"
```

2. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Launch the GUI:

```powershell
python gui_expense_tracker.py
```

## What to expect in the UI

- Main Menu: `Add Expense`, `View All Expenses`, `Analyze Expenses`, `Preferences`, `Reset Expenses`, `Exit`.
- View All Expenses screen: has a "🔙 Back" button that returns to the main menu (bottom of the view).
- Analyze Expenses screen: has a "🔙 Back" button that returns to the main menu (below the chart).
- Preferences screen: has a "🔙 Back" button and a `Save` button. Use `Save` to persist preferences and return to the main menu.

## File map (important files)

- `gui_expense_tracker.py` — app launcher
- `gui.py` — Tkinter GUI (`ExpenseTrackerGUI`) and all screens
- `storage.py` — append/load/clear/delete expenses (CSV via `csv` module)
- `analysis.py` — category aggregation + chart creation
- `config.py` — read/write `config.json` for preferences
- `utils.py` — timestamp formatting helpers
- `expenses.txt` — runtime CSV-style data file (created on first save)
- `requirements.txt` — Python dependency list
- `test_*.py` — `pytest` unit tests for non-GUI modules

## Testing

Run the test suite from the project root:

```powershell
pip install -r requirements.txt
pytest -q
```

Current tests pass locally (80 tests at time of update).

## How Back works (explicit)

All three screens that you asked about return to the main menu using `self.main_menu()` when the Back button is pressed:

- `view_expenses()` — contains `tk.Button(..., text="🔙 Back", command=self.main_menu)`
- `analyze_expenses()` — contains `tk.Button(..., text="🔙 Back", command=self.main_menu)`
- `open_preferences()` — contains `tk.Button(..., text="🔙 Back", command=self.main_menu)`

If you do not see the Back button in the running app, please verify the window size or scaling; the Back button is placed near the bottom of the screen and may be off-screen on small displays. Resize the app window to 700x500 (default) or larger.

## Troubleshooting

- If `pytest` is not found: use `python -m pytest`.
- If the GUI shows a blank area for the chart, ensure `matplotlib` and `seaborn` are installed.
- If `photo1.jpg` is missing, the app falls back to a solid background color.

## Recommended GitHub additions

- Add a `LICENSE` (e.g., MIT) to allow reuse.
- Add a small CI workflow (GitHub Actions) to run `pytest` on push; include a badge in this README.
- Add a `CONTRIBUTING.md` if you expect external contributions.

## Contributing

1. Fork the repository and create a feature branch.
2. Add tests for new behavior in `test_*.py`.
3. Open a pull request with a clear description and link to test results.

## Commit and push guidance

- Commit readable messages. Example: `git commit -m "Normalize Back labels in GUI; update README"`.
- Push to your fork and open PR against `main`.

## Contact

Open issues or PRs for bugs, feature requests, or help exporting to SQLite or a web UI.

— End of README —

- Comprehensive unit testing with pytest

  - Rationale: Validate parsing, numeric coercion, and edge cases.
  - Coverage: 39 tests covering:
    - CSV parsing (commas, quotes, newlines, special characters).
    - Numeric validation and coercion (type checking, bounds, precision).
    - Storage operations (append, load, clear, totals).
    - Edge cases (long descriptions, malformed rows, 100+ expenses).
  - Benefit: Catch bugs early and prevent regressions.

- Use of `pandas` + `seaborn` for analysis and plotting
  - Rationale: Concise aggregation and high-quality plotting with minimal code.
  - Trade-offs: Larger dependency footprint; heavier than custom implementations.

Completed improvements

✅ **CSV module integration** — Replaced naive splitting with Python's `csv` module.  
✅ **Modular refactoring** — Separated GUI, storage, and analysis into distinct modules.  
✅ **Storage abstraction** — Added path parameter to all storage functions for flexibility.  
✅ **Unit test suite** — Created an extensive pytest suite (now **71 tests** covering storage, database, import/export, backups, utils, and GUI behaviors).
✅ **Timestamps & Preferences** — Each expense now records an ISO-8601 UTC `Timestamp`; the GUI shows timestamps in local time by default and a new **Preferences** dialog lets users choose `local`, `UTC`, or a `custom` strftime format and toggle relative time display (e.g., "2h ago").
✅ **Config persistence** — Added `config.py` (persists to `config.json`) to remember UI preferences across runs.
✅ **Formatting utilities & tests** — Added `utils.py` for timezone-aware formatting and `test_utils.py` / `test_gui.py` to validate formatting and preferences behavior.

Future considerations

- SQLite for robust local storage and atomic writes.
- Import/export features (CSV/JSON) and backups.
- Custom categories and UI preferences configuration.
- Web-based interface with Flask/FastAPI and authentication.

## Technologies and tools

- Python 3.x — runtime for the application.
- Tkinter (standard library) — GUI toolkit used for windows, controls, and dialogs.
- Pillow (`pillow`) — image loading/resizing for the optional background image.
- pandas (`pandas`) — reading and aggregating expense data for analysis.
- matplotlib (`matplotlib`) — base plotting library used by `seaborn` and for embedding figures.
- seaborn (`seaborn`) — high-level plotting for the category bar chart.

Dependencies are listed in `requirements.txt` and can be installed with `pip`.

## Installation and setup

Prerequisites

- Python 3.8+ installed with `pip` available.
- On Linux, install the OS package providing `tkinter` if it is not present (e.g., `python3-tk`).

Steps

1. Clone or download the repository and change into the project directory.

```bash
cd "d:/siam/Object-oriented final project"
```

2. (Optional but recommended) Create and activate a virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Unix/macOS
source .venv/bin/activate
```

3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
python gui_expense_tracker.py
```

Notes

- The application will create `expenses.txt` automatically in the current working directory on first save.
- Optionally place an image named `photo1.jpg` next to `gui_expense_tracker.py` to use as the background; otherwise a solid color background is used.

Optional dependencies

- `pywebview` (optional) — If installed, the application will try to open interactive Plotly charts in an embedded native window. On some platforms (notably Windows) `pywebview` may require additional native build tools; if `pywebview` is not available the app will fall back to opening interactive charts in your system web browser.
- `plotly` — Required for generating interactive charts. If `plotly` is not installed the app will still produce static charts via `matplotlib`/`seaborn`.

## Usage guide

Primary workflows

- Add an expense

  1. Launch the app.
  2. Click `Add Expense` and choose a category (the project includes `Food`, `Rent`, `Utilities`, `Shopping`).
  3. Enter an `Amount` (numeric) and an optional `Description` and click OK.
  4. The entry is appended to `expenses.txt` immediately.

- View all expenses

  1. Click `View All Expenses` from the main menu.
  2. The table shows rows parsed from the storage file and displays the total spent.

- Analyze expenses

  1. Click `Analyze Expenses` to see a bar chart of total spent per category.
  2. The chart is generated by loading `expenses.txt` with `pandas` and plotting totals using `seaborn`.

- Reset (clear) expenses
  1. Click `Reset Expenses` and confirm the prompt to truncate `expenses.txt`.

Behavioral notes

- The application validates that `Amount` is numeric and will display an error dialog for invalid input.
- Lines in `expenses.txt` that do not split into three parts are skipped when viewing.

## Features

- Add expense entries with category, amount (numeric), and description.
- **Robust CSV storage** — Descriptions can contain commas, quotes, and special characters.
- Persistent storage via `expenses.txt` (append-on-save behavior).
- Tabular view of stored expenses with computed total.
- Category-wise aggregation and embedded bar chart for basic analysis.
- Reset/clear saved expenses from the GUI.
- Optional background image display using `photo1.jpg`.
- **Comprehensive unit tests** — 39 tests validating parsing, numeric coercion, and edge cases.
- **Modular design** — Separate modules for storage, analysis, and GUI (testable and reusable).

## Limitations and known issues

- Concurrency and atomicity

  - Appending to a plain text file is not protected against concurrent writes.
  - The app is single-user by design, so this is acceptable for local use.
  - Recommendation: Use SQLite for multi-user or high-concurrency scenarios.

- Database

  - Storage is file-based (CSV format) rather than database-backed.
  - Good for: Small datasets, local use, human-readable data.
  - Consider SQLite if: Concurrent writes, complex queries, or atomic transactions are needed.

- Input validation

  - Validation is minimal (amount numeric).
  - Categories are hard-coded; no ability to add custom categories from UI.
  - Future: Add custom category support and enhanced validation.

- Desktop-only
  - This is a desktop GUI application, not a web application.
  - Future: Web version could be implemented with Flask/FastAPI backend.

## Future work and improvements

✅ **Completed**

- ✅ Replace naive splitting with Python's `csv` module.
- ✅ Refactor code into modules: `storage.py`, `gui.py`, `analysis.py`.
- ✅ Add storage abstraction with `load_expenses(path)`, `append_expense(...)`, `clear_expenses(path)`.
- ✅ Add unit test suite (39 tests) with pytest.

Remaining recommendations

**Medium-term**

- Migrate storage to SQLite with schema (id, category, amount, description, timestamp).
- Add import/export features (CSV/JSON) and automated backups.
- Allow custom categories and preserve UI preferences in config file.
- Add date/time tracking for each expense.

**Long-term**

- Implement web-based interface with Flask or FastAPI.
- Add user authentication and cloud synchronization.
- Multi-device support with backend API.
- Reporting and advanced analytics features.

## Learning outcomes

From implementing and reviewing this project, expected technical gains include:

- **Practical desktop GUI development** with Tkinter and `ttk` widgets.
- **File I/O patterns** for data persistence and understanding their tradeoffs.
- **CSV handling** with Python's `csv` module for robust data parsing.
- **Modular design** principles — separating concerns between data, logic, and presentation.
- **Unit testing** with pytest — writing testable code and comprehensive test suites.
- **Data aggregation and visualization** with `pandas`, `matplotlib`, and `seaborn`.
- **Class-based architecture** for GUI components and improved maintainability.
- **Type hints and documentation** for clearer code intent.
- **Error handling and validation** for robust user input processing.

Additional learning outcomes from refactoring

- Designing clear interfaces and separation of concerns.
- Writing unit tests for non-GUI logic using dependency injection (path parameters).
- Structuring testable code that doesn't depend on global state.
- Documenting APIs and expected behavior through docstrings.

## License

No license file is included in the repository. If you want to permit reuse, add a `LICENSE` file (for example, the MIT license).

## Contact and contribution

- For code improvements, refactors, or fixes, open a pull request with a clear description and tests for new behavior when applicable.
- If you want help refactoring to unit-testable modules or porting to SQLite or a web app, I can help outline the required changes and implement them.

---
