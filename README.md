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

- `gui_expense_tracker.py` — Application entry point and the GUI code.
  - Renders the Tkinter window, menus, and interaction flows.
  - Implements functions for adding an expense, viewing expenses, analyzing expenses, and resetting storage.

- `expenses.txt` — Persistent storage.
  - Each expense is stored as a single line in the file in the format: `Category,Amount,Description`.

- Third-party libraries used for analysis and presentation.
  - `pandas` is used to load the file and aggregate amounts by category.
  - `matplotlib` and `seaborn` are used to generate the bar chart embedded in the GUI.

Data flow

1. User adds an expense via the GUI. The entry is appended to `expenses.txt` as a newline in CSV-like format.
2. Viewing reads `expenses.txt`, parses each line by splitting on commas, and populates a `ttk.Treeview` table in the GUI.
3. Analysis reads `expenses.txt` with `pandas.read_csv`, coerces `Amount` to numeric, groups by `Category`, and plots the aggregated totals.

## Design decisions and architecture

Key choices

- Plain-text file for persistence
  - Rationale: simplicity and minimal setup for academic demonstration and grading.
  - Trade-offs: no atomic transactions, limited handling of delimiters inside fields, and limited performance for large datasets.

- Single-file GUI implementation
  - Rationale: keeps the project easy to run and review.
  - Trade-offs: reduced modularity and testability; business logic is mixed with UI code.

- Use of `pandas` + `seaborn` for analysis and plotting
  - Rationale: concise aggregation and high-quality plotting with minimal code.
  - Trade-offs: larger dependency footprint; heavier than a lightweight custom aggregation + `matplotlib` only.

Alternatives considered

- CSV module for safer parsing and quoting (recommended next step).
- SQLite for robust local storage and better query performance.
- Refactoring into modules and classes to separate GUI, storage, and analysis logic (recommended for maintainability and unit testing).

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
- Persistent storage via `expenses.txt` (append-on-save behavior).
- Tabular view of stored expenses with computed total.
- Category-wise aggregation and embedded bar chart for basic analysis.
- Reset/clear saved expenses from the GUI.
- Optional background image display using `photo1.jpg`.

## Limitations and known issues

- Storage format
  - The file is CSV-like but the current parsing is a simple `split(',')`. Commas inside descriptions are not supported and will break parsing.

- Concurrency and atomicity
  - Appending to a plain text file is not protected against concurrent writes. The app is single-user, so this is acceptable for local use but not for multi-user scenarios.

- Test coverage
  - There are no automated tests included in the repository.

- Architecture
  - GUI, persistence, and analysis logic are implemented together in `gui_expense_tracker.py`, making unit testing and maintenance harder.

- Input validation
  - Validation is minimal (amount numeric); categories are currently hard-coded with no ability to add custom categories from the UI.

- Desktop-only
  - Despite the requested project type, this implementation is a desktop GUI application, not a web application.

## Future work and improvements

Short-term (recommended immediate tasks)

- Replace naive splitting with Python's `csv` module (handle quoting and commas in descriptions).
- Refactor code into modules: `storage.py`, `gui.py`, `analysis.py` to separate concerns and enable unit testing.
- Add a `storage` abstraction with functions: `load_expenses(path)`, `append_expense(...)`, `clear_expenses(path)` and unit tests for parsing edge cases.
- Add a small test suite (use `pytest`) to validate parsing, numeric coercion, and storage functions.

Medium-term

- Migrate storage to SQLite with a simple schema (id, category, amount, description, timestamp) to provide atomic writes and SQL-friendly queries.
- Add import/export features (CSV/JSON) and backups.
- Allow custom categories and preserve UI preferences in a small config file.

Long-term

- If a web-based interface is required, implement a server component (Flask or FastAPI) that exposes APIs for CRUD operations and moves persistence to SQLite. A web UI can then be implemented separately; this requires authentication considerations and a decision about hosting/sync.

## Learning outcomes

From implementing and reviewing this project, expected technical gains include:

- Practical experience building a desktop GUI with Tkinter and `ttk` widgets.
- File I/O patterns for simple persistence and understanding their limitations.
- Using `pandas` for lightweight data loading and aggregation.
- Embedding `matplotlib`/`seaborn` plots in a Tkinter GUI via `FigureCanvasTkAgg`.
- Basic input validation and user feedback with `tkinter.messagebox`.

Suggested additional learning outcomes if refactoring to an OOP design

- Designing clear interfaces and separation of concerns between GUI, storage, and analysis.
- Writing unit tests for non-GUI logic and using dependency injection for testability.

## License

No license file is included in the repository. If you want to permit reuse, add a `LICENSE` file (for example, the MIT license).

## Contact and contribution

- For code improvements, refactors, or fixes, open a pull request with a clear description and tests for new behavior when applicable.
- If you want help refactoring to unit-testable modules or porting to SQLite or a web app, I can help outline the required changes and implement them.

---