# AI Agent Instructions for IODEX Expense Tracker

This document gives focused, actionable guidance so an AI coding agent can be immediately productive in this repository.

## Quick Context

- **Purpose**: Desktop, single-user expense tracker using Tkinter. Entry point: `gui_expense_tracker.py`.
- **Storage**: Hybrid architecture—CSV legacy mode (`storage.py`) and modern SQLite backend (`database.py`, `ExpenseDatabase`).
- **Tests**: pytest-based; unit tests in `test_*.py` files; 80+ passing tests.

## Architecture Overview

### Core Components

| Module | Purpose | Key Points |
|--------|---------|-----------|
| `gui.py` | `ExpenseTrackerGUI` class handles all UI screens and navigation | Use `self.main_menu()` to return from subscreens; all expenses functions delegate to `storage.py` |
| `storage.py` | Legacy CSV interface; function signatures match GUI expectations | Functions return tuples `(category, amount, description, timestamp)` or lists of such; optional `path=` parameter for testing |
| `database.py` | Modern `ExpenseDatabase` class wraps SQLite operations | Returns tuples with `id` prepended: `(id, category, amount, description, timestamp)` |
| `analysis.py` | Chart generation (matplotlib/seaborn) and optional Plotly interactive charts | Has both CSV (`get_category_totals`) and DB (`get_category_totals_db`) variants |
| `config.py` | Persists user preferences to `config.json` (timezone, display format) | Loaded on GUI startup |
| `utils.py` | Timestamp formatting and relative time display helpers | Converts ISO-8601 UTC to user preferences via `format_iso_timestamp()` |

### Data Flow

1. **Add Expense**: GUI form → `storage.append_expense(category, amount, desc, timestamp)` → CSV file written
2. **View Expenses**: Load from file → GUI table widget with delete buttons
3. **Analyze**: Aggregate by category → matplotlib bar chart in Tkinter canvas
4. **Delete**: Match by `(category, amount, description, timestamp)` tuple → rewrite CSV without matched row
5. **Timestamps**: Stored as ISO-8601 UTC strings; displayed per user config (local/UTC/custom format)

## Key Patterns & Conventions

### Storage & Testing
- **Storage abstraction**: All `storage.py` functions accept optional `path=DEFAULT_FILENAME` parameter—pass tempfile path in tests instead of modifying `expenses.txt`.
- **Return format from `load_expenses()`**: List of tuples `[(cat, amt, desc, ts), ...]`; not dicts. GUI code assumes tuple unpacking.
- **CSV robustness**: Descriptions may contain commas, quotes, newlines—Python `csv` module handles escaping.
- **Delete matching**: `delete_expense()` matches first occurrence of tuple `(category, amount, description, [timestamp])`. Numeric tolerance for amount: `abs(amt - expected) < 1e-6`.

### GUI Conventions
- **Navigation**: Every subscreen calls `self.main_menu()` on Back button to return to main menu.
- **Filepath parameter**: `ExpenseTrackerGUI.__init__(root, filepath)` sets `self.filepath`; passed to storage functions.
- **Preview helpers**: `compute_preview_text(sample_iso, mode, custom_fmt, show_rel, tz_name)` is a testable non-GUI helper used for timestamp preview in preferences screen.

### Timestamps
- **Storage**: ISO-8601 UTC (e.g., `"2025-01-05T14:30:00+00:00"`), always timezone-aware.
- **Display**: Converted on demand via `utils.format_iso_timestamp(iso_str, mode, custom_fmt, show_relative, tz_name)` per user config.
- **Default mode**: Read from `config.json` → `config["timestamp_display"]` (values: `"local"`, `"utc"`, `"custom"`, `"relative"`).

## Developer Workflows

```powershell
# Run app
python gui_expense_tracker.py

# Run all tests
python -m pytest -q

# Run specific test file
python -m pytest test_storage.py -v

# Setup venv
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Integration Points & Optional Dependencies

- **Required**: `tkinter` (bundled), `pandas`, `matplotlib`, `seaborn`, `pillow` (fallback if no background image).
- **Optional**: `plotly` + `pywebview` enable interactive Plotly charts; code guards with try/except and gracefully falls back to matplotlib.
- **Database**: `sqlite3` (stdlib); `database.py` provides modern persistence layer not yet fully integrated into GUI.

## Common Changes

| Task | Location | Notes |
|------|----------|-------|
| Add/modify screens | `gui.py` → `ExpenseTrackerGUI` methods | Extract business logic to `storage.py` / `analysis.py` for testability |
| Storage schema | `storage.py` function signatures + `test_storage.py` | Maintain backward compat: return tuple format unchanged |
| Charts/analysis | `analysis.py` | Both CSV and DB-backed variants; optional Plotly integration |
| User preferences | `config.py` → `config.json` | Persist to disk on change; reload on startup |

## Examples from Codebase

1. **Delete workflow** (via GUI):
   - User clicks row in `view_expenses()` table, clicks Delete
   - `_delete_selected()` extracts tuple `(cat, amt, desc, ts)`
   - Calls `storage.delete_expense(cat, amt, desc, ts, path=self.filepath)`
   - CSV rewritten; table refreshed

2. **Timezone preview** (preferences screen):
   - User selects timezone → calls `compute_preview_text(sample_iso, mode, custom_fmt, show_rel, tz_name)`
   - Returns formatted string (non-GUI helper) → displayed in label
   - On save: write to `config.json`, reload on next app launch

3. **Add expense with auto-timestamp**:
   - Form entry → `storage.append_expense(cat, amt, desc, path, timestamp=None)`
   - If `timestamp=None`, function auto-generates `datetime.now(timezone.utc).isoformat()`

## Testing Guidance

- **Unit tests for logic**: `storage.py`, `analysis.py`, `utils.py` → test with `tmp_path` fixture, pass `path=` argument.
- **GUI changes**: Extract testable helpers (e.g., `compute_preview_text()`) rather than mixing logic with Tk code.
- **No GUI tests**: Focus on business logic; skip testing Tk widgets directly.
- **Example**: `test_storage.py::TestAppendExpense::test_append_valid_expense` creates tempfile, calls `append_expense()`, validates tuple format and timezone-aware timestamp.

## Migration Note: CSV → SQLite

Project is transitioning storage layer. For now:
- **`storage.py`** = CSV-based (legacy, tested, in use)
- **`database.py`** = SQLite class (modern, optional, not yet default)
- **Analysis** has both: `get_category_totals(path)` (CSV) and `get_category_totals_db(db)` (SQLite)
- When modernizing, maintain function signatures in `storage.py` or create new abstraction layer to keep GUI unchanged.
