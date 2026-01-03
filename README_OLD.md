# 📊 IODEX — Desktop Expense Tracker

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-80%20Passing-brightgreen)
![Status](https://img.shields.io/badge/Status-Production%20Ready-blue)

**IODEX** is a **professional-grade, single-user desktop expense tracker** built with Python and Tkinter. It combines a clean, intuitive GUI with robust CSV-based storage, comprehensive testing, and powerful features for managing personal finances.

> **Perfect for**: Personal budgeting, expense tracking, financial analysis, and educational projects on GUI development and data persistence.

---

## 🎯 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Architecture & Design](#-architecture--design)
- [Configuration](#-configuration)
- [Future Roadmap](#-future-roadmap)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

### Core Functionality

- ✅ **Add Expense Entries** — Record category, amount, description, and automatic timestamp
- ✅ **View All Expenses** — Table view with running total, search, and sorting
- ✅ **Delete Expenses** — Remove individual entries with confirmation
- ✅ **Expense Analysis** — Category-wise aggregation and visual bar charts
- ✅ **Reset/Clear** — Batch delete all expenses with safety confirmation

### Advanced Features

- 🌍 **Timezone Support** — View timestamps in local timezone, UTC, or custom format
- 📅 **Timestamp Management** — ISO-8601 UTC storage with user-preferred display formats
- ⏱️ **Relative Time Display** — Show "2h ago" alongside absolute timestamps
- 💾 **Persistent Configuration** — User preferences saved to `config.json`
- 🎨 **Professional UI** — Modern Tkinter interface with responsive design
- 📈 **Interactive Charts** — Static (matplotlib) + optional interactive (Plotly) visualizations
- 🖼️ **Background Support** — Optional background images for personalization

### Data Integrity

- 🔒 **Robust CSV Storage** — Handles descriptions with commas, quotes, newlines
- 📝 **Human-Readable Format** — Plain text CSV for easy backups and auditing
- ✔️ **Input Validation** — Numeric validation, category constraints
- 🛡️ **Comprehensive Testing** — 80+ unit tests covering all logic paths

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- On Linux: `python3-tk` package (Tkinter not included by default)

### 30-Second Setup (Windows)

```powershell
# 1. Navigate to project
cd "d:/siam/Object-oriented final project"

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python gui_expense_tracker.py
```

### macOS / Linux

```bash
cd /path/to/IODEX_Expense_Tracker

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python gui_expense_tracker.py
```

✨ **That's it!** The app creates `expenses.txt` automatically on first save.

---

## 📦 Installation

### Step-by-Step Guide

#### 1. Clone or Download

```bash
git clone https://github.com/eis-1/IODEX_Expense_Tracker.git
cd IODEX_Expense_Tracker
```

#### 2. Virtual Environment (Recommended)

```bash
# Create
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate
```

#### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Dependencies:**

- `pillow` — Image handling for background support
- `pandas` — Data aggregation and analysis
- `matplotlib` — Static chart rendering
- `seaborn` — High-level statistical visualization
- `plotly` — Interactive chart generation (optional)
- `pywebview` — Native window for interactive charts (optional)

#### 4. Optional: Custom Background Image

Place a `photo1.jpg` file in the project root for a custom background. The app gracefully falls back to solid color if missing.

---

## 💡 Usage Guide

### Main Menu

After launching, you'll see the **Main Menu** with these options:

```
┌─────────────────────────────────┐
│   IODEX Expense Tracker         │
├─────────────────────────────────┤
│ ➕ Add Expense                   │
│ 📋 View All Expenses             │
│ 📊 Analyze Expenses              │
│ ⚙️  Preferences                   │
│ 🔄 Reset Expenses               │
│ ❌ Exit                           │
└─────────────────────────────────┘
```

### Workflow Examples

#### Adding an Expense

1. **Click** `Add Expense`
2. **Select Category** (Food, Rent, Utilities, Shopping, Other)
3. **Enter Amount** (numeric, e.g., 25.50)
4. **Optional**: Add description (e.g., "Lunch at café")
5. **Click OK** — Entry saved automatically with timestamp
6. **Click 🔙 Back** to return to main menu

#### Viewing Expenses

1. **Click** `View All Expenses`
2. **Table displays**:
   - Category | Amount | Description | Timestamp
   - Running total at bottom
3. **Select row** and **click Delete** to remove
4. **Click 🔙 Back** to return to main menu

#### Analyzing Spending

1. **Click** `Analyze Expenses`
2. **Bar chart displays** total by category
3. **Click Export** to save as PNG
4. **Click Interactive** to open Plotly chart (if available)
5. **Click 🔙 Back** to return to main menu

#### Configuring Preferences

1. **Click** `Preferences` from main menu
2. **Section 1**: Choose timestamp display:
   - 📍 Local time (your timezone)
   - 🌍 UTC (Coordinated Universal Time)
   - ✏️ Custom format (advanced strftime)
3. **Section 2**: Search & select timezone
   - Type city name (e.g., "london", "tokyo", "dhaka")
   - Results show format: **City, Country — GMT±X**
4. **Section 3**: Custom time format (if custom mode)
   - Available tokens: `%Y`, `%m`, `%d`, `%H`, `%M`, `%Z`
5. **Section 4**: Options
   - ⏱️ Toggle relative time display ("2h ago")
6. **Section 5**: Preview
   - Live preview shows how timestamps will appear
7. **Click 💾 Save** to persist preferences
8. **Click 🔙 Back** to return without saving

#### Resetting Expenses

1. **Click** `Reset Expenses` from main menu
2. **Confirm** deletion (cannot be undone)
3. All expenses cleared from `expenses.txt`

---

## 📁 Project Structure

````
IODEX_Expense_Tracker/
├── gui_expense_tracker.py          # 🚀 Application entry point
├── gui.py                          # 🎨 Tkinter GUI (main class: ExpenseTrackerGUI)
├── storage.py                      # 💾 CSV persistence layer
├── analysis.py                     # 📊 Data aggregation & charting
├── config.py                       # ⚙️  Config file management
├── utils.py                        # 🔧 Utilities (timestamps, formatting)
├── import_export.py                # 📤 CSV/JSON import-export
├── backup.py                       # 🔄 Backup utilities
├── database.py                     # 🗄️  Database helpers (optional)
├── expenses.txt                    # 📝 Runtime data file (auto-created)
├── config.json                     # 🔐 User preferences (auto-created)
├── photo1.jpg                      # 🖼️  Background image (optional)
│
├── requirements.txt                # 📦 Python dependencies
├── README.md                       # 📖 This file
├── REFACTORING_SUMMARY.md          # 📋 Refactoring history
├── TESTING_GUIDE.md                # 🧪 Testing documentation
├── TEST_RESULTS.md                 # ✅ Latest test results
│
├── test_storage.py                 # 🧪 Storage tests
├── test_analysis_plotly.py         # 🧪 Analysis & plotting tests
├── test_gui.py                     # 🧪 GUI behavior tests
├── test_database.py                # 🧪 Database tests
├── test_utils.py                   # 🧪 Utility function tests
├── test_utils_tz.py                # 🧪 Timezone handling tests
├── test_utils_fuzzy.py             # 🧪 Fuzzy time parsing tests
│
├── .github/
│   └── copilot-instructions.md     # 🤖 AI coding agent guidelines
│
└── .git/                           # 🔗 Git repository

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
````

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
