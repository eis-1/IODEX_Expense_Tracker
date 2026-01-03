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

Run the test suite with pytest (recommended inside a virtualenv):

```powershell
pip install -r requirements.txt
pytest -q
```

The repository contains unit tests for storage, utils, analysis, and other non-GUI logic. GUI tests are provided where feasible but are light-weight.

## Development notes

- Storage uses Python's `csv` module for robust reading/writing of `expenses.txt`.
- All storage functions accept an optional `path` argument to enable tests to use temporary files.
- Timestamps are recorded as ISO-8601 in UTC; the GUI converts to local time according to `config.py` settings.
- If you plan to extend the project, consider migrating to SQLite for atomic writes and queries.

## Contributing

Contributions are welcome. Please follow these guidelines:

- Fork the repo and create a feature branch.
- Add tests for any new functionality or bugfixes.
- Keep changes focused and include a clear pull request description.
- Run `pytest` locally before submitting.

If you'd like help splitting the GUI into smaller testable components or porting storage to SQLite, I can help implement it.

## Security & privacy

- This application stores data locally in `expenses.txt`. Do not commit personal data to version control.
- There is no authentication or encryption — treat this as a personal, local tool.

## License

No license is included. If you would like to permit reuse, add a `LICENSE` file (for example, MIT). If you'd like, I can add a default license for you.

## Contact

Open issues or PRs in this repository for bugs and feature requests. If you'd like me to:

- run the test suite,
- commit these README changes, or
- add a license and CI config,
  tell me which and I'll proceed.

## IODEX — Expense Tracker (Desktop GUI)

A compact desktop expense-tracking application implemented with Python and Tkinter. The program records simple expense entries to a local text file, provides a view of saved records, and offers a basic category-based analysis (bar chart). This repository contains the application source, runtime dependencies, and the plain-text data file used for persistence.

## Project background and motivation

This project was developed as an academic final project with the intent to demonstrate practical software development skills and basic data analysis. The immediate motivation was to implement a minimal, self-contained expense tracker that illustrates GUI development, file-based persistence, and simple data aggregation/visualization. The implementation targets a single-user, local environment and does not attempt to provide multi-user, networked, or production-grade guarantees.

Scope and constraints

- Single-user, local desktop application only (no web server or network sync).
- Persistent storage is a plain-text file (`expenses.txt`) in CSV-like format; no database is used.
- Dependencies are minimal and chosen for ease of plotting and data handling (`pandas`, `matplotlib`, `seaborn`).
- The implementation focuses on functionality and demonstration rather than scalability, performance tuning, or security-hardening.

## Objectives

- Functional

  - Allow the user to add expense entries consisting of a category, an amount, and an optional description.
  - Show all recorded expenses in a tabular view and compute the total spent.
  - Produce a category-wise bar chart of total expenses for simple analysis.
  - Provide a way to clear all stored expenses.

- Technical
  - Use standard Python tooling and libraries available via `pip`.
  - Keep the application single-file and easy to run for grading and demonstration.
  - Provide clear, inspectable data output in a simple text format.

## System overview

Major components

- `gui_expense_tracker.py` — Application entry point.

  - Simplified launcher that initializes and runs the application.
  - Imports the modular components below.

- `gui.py` — User Interface module (class-based).

  - `ExpenseTrackerGUI` class encapsulates all Tkinter UI logic.
  - Separated from business logic for improved testability and maintainability.
  - Methods for each screen: `main_menu()`, `view_expenses()`, `analyze_expenses()`, etc.

- `storage.py` — Data Persistence module.

  - `append_expense(category, amount, description, path)` — Add a single expense.
  - `load_expenses(path)` — Load all expenses from file.
  - `get_total_spent(path)` — Calculate total amount spent.
  - `clear_expenses(path)` — Delete all expense records.
  - `file_exists(path)` — Check if storage file exists.
  - All functions accept optional `path` parameter for flexibility and testability.
  - Uses Python's `csv` module for robust CSV parsing and writing.

- `analysis.py` — Data Analysis module.

  - `get_category_totals(path)` — Aggregate expenses by category.
  - `create_category_chart(path)` — Generate matplotlib figure for plotting.
  - `get_summary_stats(path)` — Compute summary statistics.
  - Separated from GUI to enable independent testing and reuse.

- `test_storage.py` — Comprehensive unit test suite.

  - 39 tests covering parsing, numeric coercion, and storage functions.
  - Uses pytest for test automation and validation.
  - Tests edge cases: commas in descriptions, quotes, newlines, special characters.

- `expenses.txt` — Persistent storage (CSV format).

  - Each expense is stored as: `Category,Amount,Description,Timestamp` (ISO-8601 UTC).
  - Timestamps are stored in UTC and displayed in the GUI in local time by default; users can change formatting in Preferences.
  - Uses proper CSV quoting to handle special characters in fields.

- Third-party libraries for analysis and visualization:
  - `pandas` — Data loading and aggregation.
  - `matplotlib` and `seaborn` — Chart generation and embedding in GUI.

Data flow

1. User adds an expense via the GUI. The entry is written to `expenses.txt` using `storage.append_expense()`.
2. Viewing reads `expenses.txt` using `storage.load_expenses()`, which properly parses CSV format.
3. Analysis uses `analysis.create_category_chart()` to aggregate and visualize expenses.
4. All data operations are separated from UI logic and can be tested independently.

## Design decisions and architecture

Key choices

- Plain-text CSV file for persistence

  - Rationale: simplicity, minimal setup, and human-readable format.
  - Implementation: Uses Python's `csv` module for robust parsing and writing.
  - Benefit: Properly handles commas, quotes, and newlines in field values.

- Modular architecture with separated concerns

  - Rationale: Improved testability, maintainability, and code reuse.
  - Structure:
    - `storage.py`: Data persistence (testable without GUI).
    - `analysis.py`: Data analysis (reusable across interfaces).
    - `gui.py`: User interface (class-based, focused on presentation).
    - `gui_expense_tracker.py`: Minimal entry point.
  - Benefit: Each module can be tested and maintained independently.

- Storage abstraction with path parameters

  - Rationale: Enables flexible file handling and testability.
  - Implementation: All storage functions accept optional `path` parameter.
  - Benefit: Allows unit tests to use temporary files without affecting production data.

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
