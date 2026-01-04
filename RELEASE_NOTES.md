IODEX Expense Tracker - Release Notes

Version: 1.0.0 (migration-to-sqlite)
Date: 2026-01-05

Highlights:

- Default storage migrated to SQLite (`expenses.db`), with safe migration tools and GUI prompt.
- Analysis functions updated to work with both CSV and SQLite backends.
- New tests added to validate CSV vs DB analysis and migration.
- PyInstaller single-file Windows executable produced for convenient distribution.

Build artifact:

- File: `dist/gui_expense_tracker.exe`
- ZIP: `dist/gui_expense_tracker.zip`
- SHA256: `93e95992da20c56172cb1ba301b5d9360455ea4789a9d182b4db292a6760e87e`

Notes:

- The EXE was built using PyInstaller 6.17.0 in a virtualenv.
- Icon `app.ico` and `photo1.jpg` were bundled into the executable.
- If you want, I can prepare a GitHub Release with the zip as an asset or push a PR with changelog and release notes.
