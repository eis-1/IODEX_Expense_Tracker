IODEX Expense Tracker - Release Notes

Version: 1.0.1 (icon-update)
Date: 2026-01-05

Highlights:

- Default storage migrated to SQLite (`expenses.db`), with safe migration tools and GUI prompt.
- Analysis functions updated to work with both CSV and SQLite backends.
- New tests added to validate CSV vs DB analysis and migration.
- PyInstaller single-file Windows executable produced for convenient distribution.

Build artifact:

- File: `dist/gui_expense_tracker.exe`
- ZIP: `dist/gui_expense_tracker_v1.0.1.zip`
- SHA256 (exe): `042f62bac192a21bf36d47c39bfe068c4bae8316795f97a132eb7cc31c1f65f7`
- SHA256 (zip): `55d0eb162c8b16854f372b6f79b8a086caa73fd34dc682a239dace90a3780dfc`

Notes:

- The EXE was built using PyInstaller 6.17.0 in a virtualenv.
- Icon `app.ico` and `photo1.jpg` were bundled into the executable.
- If you want, I can prepare a GitHub Release with the zip as an asset or push a PR with changelog and release notes.
