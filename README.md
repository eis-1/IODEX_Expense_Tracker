# 📊 IODEX — Desktop Expense Tracker

![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![License](https://img.shields.io/badge/License-MIT-green) ![Tests](https://img.shields.io/badge/Tests-84%20Passing-brightgreen) ![Status](https://img.shields.io/badge/Status-Production%20Ready-blue)

IODEX is a single-user, desktop expense tracker written in Python with a simple Tkinter GUI and a robust storage layer. The app uses an SQLite database (`expenses.db`) as the default storage backend and provides helpers to migrate from the legacy CSV file format (`expenses.txt`) when present.

This repository contains the application, packaging helpers for Windows (PyInstaller), unit tests (pytest), and utility scripts for migrating and exporting data.

---

## 🎯 Quick Navigation

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [Testing](#-testing)
- [Packaging & Release](#-packaging--release)
- [Migration](#-migration)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [Troubleshooting](#-troubleshooting)
- [License](#-license)

---

## ✨ Features

- Add, view, and delete expense entries (category, amount, description, timestamp) ✅
- Defaults to SQLite (`expenses.db`) for reliable persistence; CSV (`expenses.txt`) is supported for legacy imports ✅
- Category-wise analysis and charts (matplotlib; optional plotly) 📊
- Timezone-aware timestamps and relative time display 🌍
- Preferences persisted to `config.json` (timezone, display format) ⚙️
- Tests cover storage, analysis, utils, and CLI helpers (pytest) ✅

---

## 🚀 Quick Start

1. Clone repository:

```bash
git clone https://github.com/eis-1/IODEX_Expense_Tracker.git
cd IODEX_Expense_Tracker
```

2. Create and activate virtual environment (Windows):

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the app:

```bash
python gui_expense_tracker.py
```

The app will create `expenses.db` on first run. If a legacy `expenses.txt` file exists in the project directory, you will be prompted to migrate its data to the database.

---

## 🧩 Installation & Dependencies

Install dependencies via pip:

```bash
pip install -r requirements.txt
```

Main packages used:

- `tkinter` — GUI (bundled with Python)
- `pillow` — Image handling
- `pandas`, `matplotlib`, `seaborn` — Analysis & charts
- `pytest` — Tests
- `pyinstaller` — Packaging into Windows EXE (developer only)

---

## 💡 Usage Guide

### Main Workflows

- Add Expense: Main Menu → Add Expense → fill form → Save
- View Expenses: Main Menu → View All Expenses → delete rows if needed
- Analyze: Main Menu → Analyze Expenses → category totals and bar chart
- Preferences: set timezone and timestamp display format (local/utc/custom/relative)

Timestamps are stored as ISO-8601 UTC strings and displayed as configured (see `utils.format_iso_timestamp`).

---

## 🏗 Project Structure

Key files:

- `gui_expense_tracker.py` — Application entry point
- `gui.py` — `ExpenseTrackerGUI` (Tkinter screens)
- `storage.py` — Public storage API (keeps CSV-compatible function signatures)
- `database.py` — `ExpenseDatabase` SQLite wrapper used by analysis and migration
- `analysis.py` — Chart generation and aggregation helpers
- `utils.py` — Helpers (resource_path, timestamp formatting)
- `migrate_to_db.py` — CLI migration helper
- `requirements.txt` — Python package dependencies
- `tests/` & `test_*.py` — pytest suite

---

## 🧪 Testing

Run the test suite locally:

```bash
python -m pytest -q
# Expected: 84 passed
```

All tests passed locally during verification.

---

## 📦 Packaging & Release

A Windows single-file executable is produced using PyInstaller. Build helper and a PowerShell script are included:

- `build_exe.ps1` — wrapper to run PyInstaller with required `--add-data` flags
- `utils.resource_path()` — helper so bundled assets (images, icons) are accessible when frozen

Artifacts produced locally:

- `dist/gui_expense_tracker.exe` (EXE)
- `dist/gui_expense_tracker_v1.0.1.zip` (zipped EXE)

Checksums (local build):

- EXE SHA256: `042f62bac192a21bf36d47c39bfe068c4bae8316795f97a132eb7cc31c1f65f7`
- ZIP SHA256: `55d0eb162c8b16854f372b6f79b8a086caa73fd34dc682a239dace90a3780dfc`

Note: I attempted to push the `v1.0.1` tag and create the Release, but pushes for the new tag failed due to intermittent network errors; `v1.0.0` tag was pushed successfully earlier.

If you want, I can publish the Release (attach the ZIP) if you provide a GitHub token (GITHUB_TOKEN env) or allow me to use `gh` on your machine.

---

## 🔀 Migration from CSV

If you have a legacy `expenses.txt` CSV file, the app detects it and prompts you to migrate. Alternatively, use the CLI:

```bash
python migrate_to_db.py --path expenses.txt
```

Migration preserves timestamps and descriptions (including commas/newlines) and writes entries into `expenses.db`.

---

## ⚙️ Configuration

User preferences are stored in `config.json` and include:

- `timestamp_display`: `local`, `utc`, `custom`, `relative`
- `timezone`: IANA zone name (e.g., `Europe/London`)

---

## 🛠 Troubleshooting

- If the GUI fails to start: ensure `tkinter` is available (on Linux, install `python3-tk`).
- If the PyInstaller EXE fails: ensure required runtime libs (Tk, matplotlib backends) are present and run the app from the console to view messages.

---

## 🤝 Contributing

Contributions are welcome — open a PR with a clear description and tests for new behavior.

---

## 📄 License

MIT

---

If you'd like, I can also publish the GitHub Release and attach the v1.0.1 ZIP (requires network/token).

---

## ✨ Features

### Core Functionality

- ✅ **Add Expense Entries** — Record category, amount, description, and automatic timestamp
- ✅ **View All Expenses** — Table view with running total, delete functionality
- ✅ **Delete Expenses** — Remove individual entries with confirmation
- ✅ **Expense Analysis** — Category-wise aggregation and visual bar charts
- ✅ **Reset/Clear** — Batch delete all expenses with safety confirmation

### Advanced Features

- 🌍 **Timezone Support** — View timestamps in local timezone, UTC, or custom format
- 📅 **Timestamp Management** — ISO-8601 UTC storage with user-preferred display formats
- ⏱️ **Relative Time Display** — Show "2h ago" alongside absolute timestamps
- 💾 **Persistent Configuration** — User preferences saved to `config.json`
- 🎨 **Modern UI** — Clean Tkinter interface with organized screens
- 📈 **Interactive Charts** — Static (matplotlib) + optional interactive (Plotly) visualizations
- 🖼️ **Background Support** — Optional custom background images
- 🔒 **Robust CSV Storage** — Handles descriptions with commas, quotes, newlines

### Data Integrity

- ✔️ **Input Validation** — Numeric validation, category constraints
- 📝 **Human-Readable Format** — Plain text CSV for easy backups and auditing
- 🛡️ **Comprehensive Testing** — 80+ unit tests covering all logic paths

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+** installed
- **pip** package manager
- On Linux: `python3-tk` package

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

✨ **That's it!** The app creates `expenses.db` automatically on first run. If a legacy `expenses.txt` file is found, you'll be prompted to migrate your data to the new database.

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

**What gets installed:**

- `pillow` — Image handling for background support
- `pandas` — Data aggregation and analysis
- `matplotlib` — Static chart rendering
- `seaborn` — High-level statistical visualization
- `plotly` — Interactive chart generation (optional)
- `pywebview` — Native window for interactive charts (optional)

#### 4. Optional: Custom Background Image

Place a `photo1.jpg` file in the project root for a custom background. The app gracefully falls back to solid color if missing.

#### Verify Installation

```bash
python -m pytest -q
# Should show: 80 passed
```

---

## 💡 Usage Guide

### Main Menu

After launching, you'll see the **Main Menu**:

```
⚙️ IODEX Expense Tracker
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
➕ Add Expense
📋 View All Expenses
📊 Analyze Expenses
⚙️  Preferences
🔄 Reset Expenses
❌ Exit
```

### Workflow 1: Adding an Expense

1. **Click** `➕ Add Expense`
2. **Select Category** from the list:
   - Food
   - Rent
   - Utilities
   - Shopping
   - Other
3. **Enter Amount** (e.g., 25.50)
4. **Optional**: Add description (e.g., "Lunch at café")
5. **Click OK** — Entry saved automatically with timestamp
6. **Click 🔙 Back** to return to main menu

### Workflow 2: Viewing Expenses

1. **Click** `📋 View All Expenses`
2. **Table displays:**
   - Category | Amount | Description | Timestamp
   - Running total at bottom
3. **Select row** and **click Delete** to remove
4. **Click 🔙 Back** to return to main menu

**Timestamp Display:**

- Shown based on Preferences setting (Local/UTC/Custom)
- Example: `2026-01-03 12:30:00 +06:00` or `2h ago`

### Workflow 3: Analyzing Spending

1. **Click** `📊 Analyze Expenses`
2. **Bar chart displays** total spent per category
3. **Options:**
   - **Export** — Save chart as PNG image
   - **Interactive** — Open Plotly chart (if installed)
4. **Click 🔙 Back** to return to main menu

Quick script: generate & save a chart from the DB

```python
# demo_chart.py
from analysis import create_category_chart
fig = create_category_chart('expenses.db')  # uses SQLite DB by default
fig.savefig('category_chart.png')
print('Saved category_chart.png')
```

Run it with:

```bash
python demo_chart.py
```

### Workflow 4: Configuring Preferences

1. **Click** `⚙️ Preferences` from main menu
2. **Section 1: Timestamp Display Mode**
   - 📍 Local time (your timezone)
   - 🌍 UTC (Coordinated Universal Time)
   - ✏️ Custom format (advanced strftime)
3. **Section 2: Timezone Selection**
   - Type city name (e.g., "london", "tokyo", "dhaka")
   - Results show: **City, Country — GMT±X**
   - Click to select timezone
4. **Section 3: Custom Time Format** (if custom mode selected)
   - Available tokens: `%Y`, `%m`, `%d`, `%H`, `%M`, `%Z`
   - Example: `%Y-%m-%d %H:%M:%S %Z`
5. **Section 4: Display Options**
   - ⏱️ Toggle relative time display ("2h ago")
6. **Section 5: Live Preview**
   - See exactly how timestamps will appear
7. **Click 💾 Save** to persist preferences
8. **Click 🔙 Back** to cancel and return

### Workflow 5: Resetting Expenses

1. **Click** `🔄 Reset Expenses` from main menu
2. **Confirm** deletion (⚠️ cannot be undone)
3. All expenses cleared from your current storage file (by default, `expenses.db`)

---

## 📁 Project Structure

```
IODEX_Expense_Tracker/
├── gui_expense_tracker.py          # 🚀 Application entry point
├── gui.py                          # 🎨 Tkinter GUI implementation
├── storage.py                      # 💾 Hybrid CSV/SQLite persistence layer
├── analysis.py                     # 📊 Data aggregation & charting
├── config.py                       # ⚙️  Config file management
├── utils.py                        # 🔧 Utilities & helpers
├── import_export.py                # 📤 CSV/JSON import-export
├── backup.py                       # 🔄 Backup utilities
├── database.py                     # 🗄️  Database helpers
│
├── expenses.db                     # 🗄️  SQLite database (default)
├── expenses.txt                    # 📝 Legacy CSV data file (optional)
├── config.json                     # 🔐 User preferences (auto-created)
├── photo1.jpg                      # 🖼️  Background image (optional)
│
├── requirements.txt                # 📦 Python dependencies
├── README.md                       # 📖 This file
├── REFACTORING_SUMMARY.md          # 📋 Refactoring history
├── TESTING_GUIDE.md                # 🧪 Testing documentation
│
├── test_storage.py                 # 🧪 Storage tests
├── test_analysis_plotly.py         # 🧪 Analysis tests
├── test_gui.py                     # 🧪 GUI behavior tests
├── test_database.py                # 🧪 Database tests
├── test_utils.py                   # 🧪 Utility tests
├── test_utils_tz.py                # 🧪 Timezone tests
├── test_utils_fuzzy.py             # 🧪 Fuzzy parsing tests
│
├── .github/
│   └── copilot-instructions.md     # 🤖 AI coding guidelines
│
└── .git/                           # 🔗 Git repository
```

### File Descriptions

| File                     | Purpose                                                              |
| ------------------------ | -------------------------------------------------------------------- |
| `gui_expense_tracker.py` | Application launcher — runs the Tkinter event loop                   |
| `gui.py`                 | Main GUI class (`ExpenseTrackerGUI`) with all screens                |
| `storage.py`             | Hybrid CSV/SQLite persistence — append, load, delete, clear expenses |
| `analysis.py`            | Data aggregation and chart generation                                |
| `config.py`              | Config file management — read/write `config.json`                    |
| `utils.py`               | Utilities — timestamps, formatting, validation                       |
| `import_export.py`       | CSV/JSON import-export helpers                                       |
| `backup.py`              | Backup and recovery utilities                                        |
| `database.py`            | Optional database schema helpers                                     |

---

## 🧪 Migration & Testing

### Migrating Legacy Data

If you have an old `expenses.txt` file, the app will prompt you to migrate your data to the new `expenses.db` database on first run. You can also migrate manually using the CLI tool:

```bash
python migrate_to_db.py --src expenses.txt --dst expenses.db
```

This will import all your legacy expenses into the database, preserving timestamps and descriptions.

Quick GUI migration flow:

1. Start the app (`python gui_expense_tracker.py`).
2. If a legacy `expenses.txt` is detected, you'll see a **Migrate Now** prompt.
3. Click **Migrate Now** to run the migration (safe & non-destructive).

Example: Verify migration

```bash
# After migration, list totals via the database helper
python -c "from database import ExpenseDatabase; db=ExpenseDatabase('expenses.db'); print(db.get_category_totals())"
```

IODEX includes **comprehensive test coverage**:

### Running Tests

```bash
# Install pytest (if not in requirements.txt)
pip install pytest

# Run all tests
pytest -q

# Run with verbose output
pytest -v

# Run specific test file
pytest test_storage.py -v

# Run with coverage report
pip install pytest-cov
pytest --cov=. --cov-report=html
```

### Test Results

- **Total Tests**: 80+ test cases
- **Status**: ✅ All passing
- **Execution Time**: < 10 seconds
- **Coverage**: All core modules (storage, analysis, utils, gui)

---

## 📦 Creating a standalone Windows .exe (PyInstaller)

You can create a single-file Windows executable using PyInstaller. The project already includes a small helper `utils.resource_path()` so packaged apps can locate assets like `photo1.jpg` at runtime.

PowerShell one-liner (recommended from project root with virtualenv activated):

```powershell
# Install PyInstaller if needed
python -m pip install --upgrade pyinstaller

# Create a single-file, windowed executable and include the image asset
pyinstaller --noconfirm --clean --onefile --windowed --add-data "photo1.jpg;." gui_expense_tracker.py
```

Or use the provided helper script:

```powershell
.\.\build_exe.ps1
```

Note:

- The `--add-data "photo1.jpg;."` flag tells PyInstaller to include the image and extract it next to the app at runtime. On Windows the separator is `;`, on macOS/Linux use `:`.
- If your app needs other data files, add them with additional `--add-data` flags (e.g., `--add-data "config.json;."`).

Prebuilt Windows executable

A prebuilt Windows executable and zip archive were created in this workspace for quick testing:

- `dist/gui_expense_tracker.exe` — single-file executable built with PyInstaller
- `dist/gui_expense_tracker.zip` — zipped EXE for easy download

If you want this included as a GitHub release asset or attached to a PR, I can prepare and upload it for you.

Resource helper (already added to `utils.py`):

```python
# utils.resource_path
import sys, os

def resource_path(relative_path: str) -> str:
    """Return absolute path to bundled resource.

    When running as a PyInstaller bundle, resources are available under
    `sys._MEIPASS`. Otherwise resolve relative to the module.
    """
    if getattr(sys, 'frozen', False):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)
```

### Test Files

| File                      | Focus                                        | Coverage |
| ------------------------- | -------------------------------------------- | -------- |
| `test_storage.py`         | CSV parsing, storage operations, edge cases  | ✅       |
| `test_analysis_plotly.py` | Data aggregation, matplotlib/plotly charting | ✅       |
| `test_gui.py`             | GUI screen behavior, preferences, navigation | ✅       |
| `test_database.py`        | Database schema and operations               | ✅       |
| `test_utils.py`           | Timestamp formatting, validation             | ✅       |
| `test_utils_tz.py`        | Timezone detection and conversion            | ✅       |
| `test_utils_fuzzy.py`     | Fuzzy time parsing and matching              | ✅       |

### Key Test Coverage Areas

✅ CSV parsing with special characters (commas, quotes, newlines)
✅ Numeric validation and coercion
✅ Storage operations (append, load, delete, clear)
✅ Timezone handling and formatting
✅ Chart generation and analysis
✅ GUI widget behavior and interaction
✅ Config persistence and defaults
✅ Edge cases (100+ expenses, malformed data, invalid input)

---

## 🏗️ Architecture & Design

### Layered Architecture

```
┌──────────────────────────────────────────┐
│         GUI Layer (gui.py)               │
│    Tkinter UI, User Interaction          │
├──────────────────────────────────────────┤
│    Business Logic & Analysis             │
│  storage.py│analysis.py│config.py│utils.py
├──────────────────────────────────────────┤
│       Data Persistence Layer             │
│   SQLite DB (expenses.db) | CSV (legacy) │
└──────────────────────────────────────────┘
```

### Key Design Principles

1. **Separation of Concerns** — GUI, business logic, and storage cleanly separated
2. **Testability** — Storage functions accept optional `path` parameter for testing
3. **Robustness** — CSV module used instead of string splitting
4. **Modularity** — Each module has single, well-defined responsibility
5. **Error Handling** — Graceful fallbacks (missing images, invalid dates)

### Main Classes

#### `ExpenseTrackerGUI` (gui.py)

Core GUI class managing all screens:

- `main_menu()` — Central navigation hub
- `add_expense_menu()` — Category selection
- `category_input()` — Form entry for amount/description
- `view_expenses()` — Table view with delete
- `analyze_expenses()` — Chart generation
- `open_preferences()` — User settings (timestamp, timezone, format)

#### Storage Functions (storage.py)

CSV-based persistence:

- `append_expense(...)` — Add entry
- `load_expenses(path)` — Parse all entries
- `delete_expense(...)` — Remove entry
- `clear_expenses(path)` — Truncate file
- `get_total_spent(path)` — Sum all amounts

#### Analysis Functions (analysis.py)

Data aggregation and visualization:

- `analyze_by_category(expenses)` — Group by category
- `create_chart(expenses, chart_type)` — Generate matplotlib chart
- `create_interactive_chart(expenses)` — Generate Plotly chart

#### Utils Functions (utils.py)

Helpers and utilities:

- `build_timezone_registry()` — Load 450+ timezones with GMT offsets
- `format_iso_timestamp(...)` — Format per user preferences
- `parse_iso_to_local_dt(...)` — Convert ISO to local time

---

## ⚙️ Configuration

### User Preferences (config.json)

User preferences are automatically saved:

```json
{
  "timestamp_mode": "local",
  "timezone": "Asia/Dhaka",
  "custom_format": "%Y-%m-%d %H:%M:%S %Z",
  "show_relative": true
}
```

**Options:**

- `timestamp_mode` — `"local"`, `"utc"`, or `"custom"`
- `timezone` — Any IANA timezone (e.g., `"America/New_York"`)
- `custom_format` — strftime format string
- `show_relative` — Display relative times (boolean)

### Timezone Support

**Built-in Timezone Search:**

- 450+ worldwide timezones
- Search by city name: "london", "tokyo", "dhaka"
- Display format: **City, Country — GMT±X**
- Smart prefix and substring matching

**Example Timezones:**

```
Dhaka, Asia — GMT+6
London, Europe — GMT+0
New York, America — GMT-5
Sydney, Australia — GMT+11
Dubai, Asia — GMT+4
Tokyo, Asia — GMT+9
Paris, Europe — GMT+1
```

---

## 📊 Data Format

### Expenses Database (expenses.db)

The default storage is now a SQLite database. Legacy CSV format is still supported for backward compatibility and migration.

```csv
Food,15.50,Lunch at café,2026-01-03T12:30:00+00:00
Rent,500.00,January rent payment,2026-01-03T10:00:00+00:00
Utilities,45.75,"Electric bill, water, gas",2026-01-02T14:22:00+00:00
Shopping,120.00,"Clothes and shoes",2026-01-01T09:15:00+00:00
```

**Columns:**

1. **Category** — Food, Rent, Utilities, Shopping, Other
2. **Amount** — Numeric value (decimal allowed)
3. **Description** — Free text (safely handles special characters)
4. **Timestamp** — ISO-8601 UTC format

**Why SQLite?**

- ✅ Fast, reliable, and scalable
- ✅ Supports advanced queries and analysis
- ✅ No manual file management needed
- ✅ Easy migration from legacy CSV
- ✅ Data integrity and atomic operations

**CSV remains supported for legacy data and import/export.**

---

## � Changelog (Recent Changes)

- **Default storage switched to SQLite (`expenses.db`)** for improved performance and reliability while keeping backward compatibility with legacy CSV (`expenses.txt`). ✅
- **Migration tools added**: a GUI prompt on first run and a CLI tool `migrate_to_db.py` to migrate legacy CSV into the database preserving timestamps and descriptions. ✅
- **Analysis updated** to work with both CSV and SQLite backends (charts and summary statistics). ✅
- **Unit tests added** to validate CSV vs DB behavior for analysis functions and storage migration. ✅

> Tip: These changes are backwards compatible — if you prefer the old CSV file you can keep using `expenses.txt` and nothing will break.

---

## �🔮 Future Roadmap

### Short-term (Next Release)

- [ ] **Custom Categories** — Add user-defined categories
- [ ] **Date Range Filtering** — View/analyze specific periods
- [ ] **Monthly Reports** — Summary by month with trends
- [ ] **Recurring Expenses** — Automated expense entries
- [ ] **Search and Filter** — Find by keyword or amount range

### Medium-term

- [ ] **SQLite Migration** — Replace CSV with SQLite database
- [ ] **Enhanced Export**:
  - PDF reports with charts
  - Email summaries
  - Cloud backup integration
  - Excel with formatting
- [ ] **Data Import Tools**:
  - CSV bulk import
  - Bank statement parsing
  - Format converters

### Long-term

- [ ] **Web Application** — Flask/FastAPI backend with web UI
- [ ] **Mobile App** — React Native or Flutter companion
- [ ] **Cloud Sync** — Multi-device synchronization
- [ ] **Advanced Analytics**:
  - Spending trends and forecasts
  - Budget creation and alerts
  - Savings goals tracking
- [ ] **User Accounts & Sharing**:

  - Multi-user support
  - Shared expense splitting
  - Family budget management

- [ ] **Integration Options**:
  - Bank account connections
  - API for third-party apps
  - Receipt scanning (OCR)

---

## 🐛 Troubleshooting

| Issue                           | Solution                                                                          |
| ------------------------------- | --------------------------------------------------------------------------------- |
| "No module named 'tkinter'"     | Install: `apt-get install python3-tk` (Linux) or `brew install python-tk` (macOS) |
| "pytest not found"              | Use `python -m pytest` instead of `pytest`                                        |
| Charts show blank               | Ensure: `pip install -r requirements.txt`                                         |
| `photo1.jpg` not showing        | Place in project root; app falls back to solid color if missing                   |
| Network connection error        | Check internet; some features need online access                                  |
| "Cannot open interactive chart" | Install: `pip install pywebview`                                                  |
| App freezes during chart        | Charts may take time on large datasets; wait for completion                       |
| Timezone search not working     | Ensure `utils.py` has latest code; run `pytest test_utils_tz.py`                  |

### Getting More Help

1. Check [TESTING_GUIDE.md](TESTING_GUIDE.md) for test-specific issues
2. Review [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) for recent changes
3. Check [TEST_RESULTS.md](TEST_RESULTS.md) for current test status
4. Open an [Issue](https://github.com/eis-1/IODEX_Expense_Tracker/issues) on GitHub

---

## 📚 Implementation Details

### Technologies Used

| Technology     | Purpose                       | Version |
| -------------- | ----------------------------- | ------- |
| **Python**     | Core language                 | 3.8+    |
| **Tkinter**    | Desktop GUI                   | stdlib  |
| **Pillow**     | Image handling                | Latest  |
| **pandas**     | Data analysis                 | Latest  |
| **matplotlib** | Static charts                 | Latest  |
| **seaborn**    | Statistical visualization     | Latest  |
| **plotly**     | Interactive charts (optional) | Latest  |
| **pywebview**  | Native windows (optional)     | Latest  |
| **pytest**     | Unit testing                  | Latest  |

### Implementation Highlights

1. **Robust CSV Handling**

   - Python's `csv` module (not string splitting)
   - Proper quoting and escaping
   - Prevents injection vulnerabilities

2. **Timezone System**

   - Built-in registry of 450+ timezones
   - Pre-computed GMT offsets
   - Smart search with prefix/substring matching

3. **Configuration Management**

   - Automatic `config.json` creation
   - User preferences preserved across sessions
   - Graceful defaults if config missing

4. **Error Handling**

   - Input validation (numeric amounts)
   - Confirmation dialogs for destructive operations
   - Fallback behaviors for missing resources

5. **Testing Strategy**
   - Unit tests for all non-GUI logic
   - Temporary file fixtures for isolation
   - Edge case coverage (100+ expenses, special characters)

---

## 🤝 Contributing

We welcome contributions! Here's how:

### To Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes with tests
4. **Run** full test suite: `pytest -v`
5. **Commit** with clear message: `git commit -m "Add feature: description"`
6. **Push** to your fork: `git push origin feature/amazing-feature`
7. **Open** a Pull Request with description

### Guidelines

- Follow PEP 8 style guidelines
- Add unit tests for new functionality
- Update README for new features
- Ensure all tests pass before submitting PR
- Keep commit messages descriptive and atomic

---

## 📝 License

This project is provided **as-is** for educational and personal use.

To allow others to use and modify this work, consider adding:

- **MIT License** — Permissive, simple
- **Apache 2.0** — Permissive, with patent clause
- **GPL** — Copyleft, source sharing required

See [choosealicense.com](https://choosealicense.com/) for details.

---

## 📞 Support & Contact

- **Found a bug?** Open an [Issue](https://github.com/eis-1/IODEX_Expense_Tracker/issues)
- **Have a feature idea?** Create a [Discussion](https://github.com/eis-1/IODEX_Expense_Tracker/discussions)
- **Want to contribute?** See [Contributing](#-contributing) above
- **Need help?** Check [Troubleshooting](#-troubleshooting)

---

## 🎓 Learning Outcomes

This project demonstrates:

- **Desktop GUI Development** — Tkinter and `ttk` widgets
- **File I/O & Persistence** — CSV handling and data formats
- **Modular Design** — Clear separation of concerns
- **Unit Testing** — Comprehensive test suites with pytest
- **Data Analysis** — Aggregation and visualization
- **Software Engineering** — Real-world practices and patterns
- **Configuration Management** — Preferences and persistence
- **Error Handling** — Robust user input processing

---

## 🙏 Acknowledgments

This project was developed as an **Object-Oriented Programming final project**, demonstrating professional-grade software engineering practices.

---

<div align="center">

**Made with ❤️ for personal finance tracking**

⭐ If you find this useful, please consider starring the repository!

[GitHub](https://github.com/eis-1/IODEX_Expense_Tracker) • [Issues](https://github.com/eis-1/IODEX_Expense_Tracker/issues) • [Discussions](https://github.com/eis-1/IODEX_Expense_Tracker/discussions)

</div>
