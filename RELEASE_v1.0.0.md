# 🚀 IODEX Expense Tracker v1.0.0 — First Official Release

A polished, feature-rich desktop expense tracker built with **Python + Tkinter**, designed with clean architecture, strong testing discipline, and practical real-world features like **SQLite storage** and **timezone-aware timestamps**.

## ✨ What’s New (v1.0.0)

- 🗄️ **SQLite-first storage** with automatic schema creation and reliable local persistence
- 🌍 **450+ timezones** with smart search + flexible timestamp display (Local / UTC / Custom)
- 📊 **Spending analysis by category** with chart export + optional interactive plotting
- 🎨 **Modernized Tkinter UI** (clean layout, improved readability, smoother workflows)
- 🧪 **80+ automated tests** (currently 84 passing) to keep changes safe and maintainable
- 🔄 **Import/Export + Backup tooling** for portability and data protection

## 🧠 Key Technical Highlights

### 🗃️ Database & Data Safety

- SQLite backend via `sqlite3`
- Crash-safety improvements (WAL mode + sensible PRAGMAs)
- Automatic creation of the `expenses` table
- Local-first design: no cloud dependency, your data stays on your machine

### 🖥️ UI & UX

- Tkinter desktop app with a clean, familiar layout
- Background image support bundled into the EXE (`photo1.jpg`)
- Analysis screen renders charts cleanly and provides Export/Interactive options

### ✅ Testing & Quality

- Extensive pytest coverage across storage, analysis, utilities, and GUI behavior
- Regression-focused fixes (e.g., deletion correctness, timestamp handling, UI stability)

## 📦 Install (Windows — pre-built EXE)

1. Download **`IODEX_Expense_Tracker.exe`** from the **Assets** section below.
2. Put it in a folder you control (example: `Documents\IODEX Expense Tracker\`).
3. Double-click to run.
4. If Windows SmartScreen appears: **More info → Run anyway**.

📝 Notes:

- The app will create local files in the same folder you run it from (for example: `expenses.db`, `config.json`).
- Logs (for troubleshooting) are written under **`%APPDATA%\IODEX_Expense_Tracker\logs\app.log`**.

## 🛠️ Build From Source (for developers)

This project supports professional packaging via PyInstaller, including bundled assets and GUI mode.

- Entry point: `gui_expense_tracker.py`
- Recommended build command is documented in the README.

## 🙌 Thank You

This release marks the first stable milestone of my Object-Oriented Programming final project, built with an emphasis on **software engineering practices**, **testability**, and a clean user experience.

---

For full changelog and technical details, see [CHANGELOG.md](CHANGELOG.md) and [README.md](README.md).
