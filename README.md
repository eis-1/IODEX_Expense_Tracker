# GUI Expense Tracker

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-80%2B%20passing-brightgreen)](TEST_RESULTS.md)

A professional, feature-rich personal expense tracker with a modern Tkinter GUI, SQLite database storage, CSV import/export, advanced timezone support, and comprehensive data analysis tools.

**Author:** MD EAFTEKHIRUL ISLAM © 2026

---

## ✨ Features

- **📊 Expense Management**: Add, view, edit, and delete expenses with ease
- **🗄️ SQLite Database**: Fast, reliable storage with automatic migrations
- **📈 Data Analysis**: Interactive charts and category-based spending insights
- **🌍 Timezone Support**: 450+ worldwide timezones with smart search
- **⏱️ Flexible Timestamps**: Local time, UTC, or custom formats
- **📤 Import/Export**: CSV and JSON support for data portability
- **🔄 Backup & Restore**: Automatic backup system for data protection
- **🎨 Modern UI**: Clean, intuitive Tkinter interface
- **🧪 Well-Tested**: 80+ unit tests with comprehensive coverage
- **📦 Portable**: Build standalone executables with PyInstaller

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Development](#-development)
- [Testing](#-testing)
- [Building Executables](#-building-executables)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

```powershell
# Clone the repository
git clone https://github.com/YOUR_USERNAME/gui-expense-tracker.git
cd gui-expense-tracker

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1  # On Windows
# source .venv/bin/activate  # On macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run the application
python gui_expense_tracker.py
```

---

## 📦 Installation

### Prerequisites

- **Python 3.10 or higher** (developed with Python 3.14)
- **pip** package manager
- **tkinter** (usually included with Python)

### Dependencies

All required packages are listed in [requirements.txt](requirements.txt):

```
pillow
pandas
matplotlib
seaborn
plotly
pywebview
```

### Install

```bash
# Install all dependencies
pip install -r requirements.txt

# Or install individually
pip install pillow pandas matplotlib seaborn plotly pywebview
```

---

## 💻 Usage

### Running the Application

```bash
python gui_expense_tracker.py
```

### Main Features

#### 1. **Add Expense**

- Select a category (Food, Rent, Utilities, Shopping, Other)
- Enter amount and description
- Timestamps are automatically recorded

#### 2. **View Expenses**

- Display all expenses in a sortable table
- Shows: Category, Amount, Description, Timestamp
- Delete expenses individually
- Running total displayed

#### 3. **Analyze Spending**

- View category-based spending charts
- Export charts as PNG images
- Interactive Plotly charts (optional)

#### 4. **Preferences**

- **Timezone**: Choose from 450+ worldwide timezones
- **Display Mode**: Local time, UTC, or custom format
- **Relative Time**: Show "2h ago" style timestamps
- **Custom Formats**: Use strftime patterns

#### 5. **Backup & Restore**

- Automatic backups before operations
- Manual backup creation
- Restore from previous backups

---

## 📁 Project Structure

```
gui-expense-tracker/
├── gui_expense_tracker.py      # Application entry point
├── gui.py                      # GUI implementation
├── database.py                 # SQLite database layer
├── storage.py                  # Legacy CSV support
├── analysis.py                 # Data analysis & charting
├── config.py                   # Configuration management
├── utils.py                    # Utility functions
├── backup.py                   # Backup utilities
├── import_export.py            # CSV/JSON import/export
├── migrate_to_db.py            # Database migration tool
│
├── requirements.txt            # Python dependencies
├── gui_expense_tracker.spec    # PyInstaller spec file
├── build_exe.ps1               # Build script for Windows
│
├── test_*.py                   # Unit tests
├── tools/                      # Helper scripts
│   └── create_icon.py          # Icon generation
│
├── README.md                   # This file
├── LICENSE                     # MIT License
├── CONTRIBUTING.md             # Contribution guidelines
├── DEVELOPER_GUIDELINES.md     # Developer documentation
├── TESTING_GUIDE.md            # Testing documentation
├── DOCUMENTATION_INDEX.md      # Documentation index
├── REFACTORING_SUMMARY.md      # Refactoring history
└── RELEASE_NOTES.md            # Release information
```

### Core Modules

| Module                   | Purpose                                     |
| ------------------------ | ------------------------------------------- |
| `gui_expense_tracker.py` | Application launcher and entry point        |
| `gui.py`                 | Main GUI class with all screens and widgets |
| `database.py`            | SQLite database operations and migrations   |
| `storage.py`             | CSV-based storage (legacy support)          |
| `analysis.py`            | Data aggregation and chart generation       |
| `config.py`              | User preferences and configuration          |
| `utils.py`               | Timestamp formatting, timezone utilities    |
| `backup.py`              | Automated backup and restore functionality  |
| `import_export.py`       | CSV and JSON import/export helpers          |

---

## 🛠️ Development

### Setting Up Development Environment

```bash
# Clone and navigate
git clone https://github.com/YOUR_USERNAME/gui-expense-tracker.git
cd gui-expense-tracker

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\Activate.ps1

# Install dependencies including dev tools
pip install -r requirements.txt
pip install pytest pytest-cov mypy ruff
```

### Code Quality

```bash
# Run linter
ruff check .

# Run type checker
mypy .

# Format code
ruff check --fix .
```

### Project Guidelines

- Follow [PEP 8](https://pep8.org/) style guidelines
- Write docstrings for all functions and classes
- Add unit tests for new features
- Update documentation when adding features
- Keep commits atomic and well-described

For detailed guidelines, see [DEVELOPER_GUIDELINES.md](DEVELOPER_GUIDELINES.md).

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest test_storage.py -v

# Run with coverage report
pytest --cov=. --cov-report=html
```

### Test Coverage

- **Total Tests**: 80+ test cases
- **Status**: ✅ All passing
- **Coverage Areas**:
  - Storage operations (CSV & SQLite)
  - Data analysis and charting
  - GUI behavior and widgets
  - Timezone handling
  - Utility functions
  - Edge cases and error handling

For detailed testing information, see [TESTING_GUIDE.md](TESTING_GUIDE.md).

---

## 📦 Building Executables

### Windows Executable

```powershell
# Install PyInstaller
pip install pyinstaller

# Recommended: build a single-file, windowed EXE with bundled assets
# IMPORTANT: --add-data uses a ';' separator on Windows: "source;dest"
pyinstaller --noconfirm --clean --onefile --windowed `
  --name "IODEX_Expense_Tracker" `
  --icon "app.ico" `
  --add-data "photo1.jpg;." `
  gui_expense_tracker.py

# Or use the build script
.\build_exe.ps1

# Or build from the spec file (advanced)
pyinstaller --clean --noconfirm gui_expense_tracker.spec
```

The executable will be created in the `dist/` directory.

### Build Configuration

The [gui_expense_tracker.spec](gui_expense_tracker.spec) file includes:

- Single-file executable configuration
- Data file inclusion (icons, images)
- Windows-specific optimizations
- Hidden imports handling

### Troubleshooting PyInstaller (pandas/plotly/matplotlib)

If the EXE builds but crashes with missing-module errors, PyInstaller may need help discovering imports.

Common fixes:

- **See exactly what's missing**:
  - Build with: `--debug=imports`
- **Add explicit hidden imports** (repeat as needed):
  - `--hidden-import <module.name>`
- **Collect submodules (useful for pandas/plotly)**:
  - `--collect-submodules pandas`
  - `--collect-submodules plotly`
- **Collect package data files** (plotly and some chart tooling may require this):
  - `--collect-data plotly`
  - `--collect-all plotly`

Tip: if you end up adding many hidden imports, put them into `gui_expense_tracker.spec` so your build stays reproducible.

---

## 📚 Documentation

### Available Documentation

- **[README.md](README.md)** - Project overview and quick start (this file)
- **[DEVELOPER_GUIDELINES.md](DEVELOPER_GUIDELINES.md)** - Development workflow and standards
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - Testing procedures and guidelines
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to the project
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Complete documentation index
- **[REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md)** - Refactoring history and decisions
- **[RELEASE_NOTES.md](RELEASE_NOTES.md)** - Version history and release notes

### Architecture Documentation

The application follows a layered architecture:

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

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### How to Contribute

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes with tests
4. **Run** the test suite: `pytest -v`
5. **Commit** your changes (`git commit -m 'Add amazing feature'`)
6. **Push** to your branch (`git push origin feature/amazing-feature`)
7. **Open** a Pull Request

### Contribution Guidelines

- Write clear, descriptive commit messages
- Add unit tests for new functionality
- Update documentation for significant changes
- Ensure all tests pass before submitting PR
- Follow existing code style and conventions

For detailed guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2026 MD EAFTEKHIRUL ISLAM

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

## 🎓 Technologies Used

- **Python 3.10+** - Core programming language
- **Tkinter** - GUI framework (standard library)
- **SQLite** - Database (via Python sqlite3 module)
- **Pandas** - Data manipulation and analysis
- **Matplotlib** - Static chart generation
- **Seaborn** - Statistical data visualization
- **Plotly** - Interactive charts (optional)
- **Pillow** - Image processing
- **PyInstaller** - Executable building

---

## 🐛 Troubleshooting

### Common Issues

| Issue                       | Solution                                                                          |
| --------------------------- | --------------------------------------------------------------------------------- |
| "No module named 'tkinter'" | Install: `apt-get install python3-tk` (Linux) or `brew install python-tk` (macOS) |
| Charts not displaying       | Ensure matplotlib is installed: `pip install matplotlib`                          |
| Database errors             | Delete `expenses.db` to create a fresh database                                   |
| Import errors               | Verify virtual environment is activated                                           |
| Test failures               | Ensure all dependencies installed: `pip install -r requirements.txt`              |

### Getting Help

- Check existing [documentation](DOCUMENTATION_INDEX.md)
- Review [test results](TEST_RESULTS.md)
- Open an [issue](https://github.com/YOUR_USERNAME/gui-expense-tracker/issues)
- Read [troubleshooting guide](DEVELOPER_GUIDELINES.md#troubleshooting)

---

## 🗺️ Roadmap

### Planned Features

- **Custom Categories**: User-defined expense categories
- **Date Range Filtering**: View expenses for specific periods
- **Recurring Expenses**: Automated recurring entry support
- **Budget Tracking**: Set and monitor budget limits
- **Multi-currency Support**: Track expenses in different currencies
- **Cloud Sync**: Optional cloud backup and sync
- **Mobile Companion**: React Native or Flutter app
- **Advanced Analytics**: Spending trends and forecasts

---

## 📞 Contact & Support

- **Author**: MD EAFTEKHIRUL ISLAM
- **Project Link**: [https://github.com/YOUR_USERNAME/gui-expense-tracker](https://github.com/YOUR_USERNAME/gui-expense-tracker)
- **Issues**: [Report bugs or request features](https://github.com/YOUR_USERNAME/gui-expense-tracker/issues)

---

## 🙏 Acknowledgments

- Developed as an Object-Oriented Programming final project
- Built with modern software engineering best practices
- Inspired by personal finance management needs

---

<div align="center">

**Made with ❤️ for better personal finance management**

⭐ **If you find this useful, please star the repository!**

[Report Bug](https://github.com/YOUR_USERNAME/gui-expense-tracker/issues) · [Request Feature](https://github.com/YOUR_USERNAME/gui-expense-tracker/issues) · [View Documentation](DOCUMENTATION_INDEX.md)

</div>
