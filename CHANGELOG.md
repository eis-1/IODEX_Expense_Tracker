# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-07

### Added

- Initial public release of GUI Expense Tracker
- **Core Features**:
  - Tkinter-based desktop GUI with modern interface
  - SQLite database for reliable data storage
  - CSV import/export functionality
  - Legacy CSV file support for backward compatibility
- **Expense Management**:
  - Add, view, edit, and delete expenses
  - Category-based organization (Food, Rent, Utilities, Shopping, Other)
  - Automatic timestamp recording
  - Running total calculations
- **Data Analysis**:
  - Category-based spending analysis
  - Matplotlib chart generation
  - Plotly interactive charts (optional)
  - Chart export as PNG images
- **Advanced Features**:
  - Timezone support for 450+ worldwide timezones
  - Smart timezone search with prefix/substring matching
  - Multiple timestamp display modes (Local, UTC, Custom)
  - Relative time display ("2h ago" style)
  - Custom strftime format support
- **Data Management**:
  - Automatic backup system
  - Manual backup creation and restore
  - Database migration tools from CSV to SQLite
  - Data validation and error handling
- **User Preferences**:
  - Persistent configuration via config.json
  - Timezone selection and customization
  - Timestamp format preferences
  - Display mode settings
- **Testing**:
  - 80+ unit tests with pytest
  - Comprehensive test coverage
  - Tests for storage, analysis, GUI, utilities, and timezone handling
  - Edge case coverage
- **Documentation**:
  - Complete README with badges and examples
  - Developer guidelines
  - Testing guide
  - Contribution guidelines
  - Documentation index
  - Release notes
  - Refactoring summary
- **Build & Deployment**:
  - PyInstaller spec file for Windows executables
  - PowerShell build script
  - GitHub Actions workflow ready
  - Comprehensive .gitignore

### Technical Details

- **Python Version**: 3.10+ (developed with 3.14)
- **GUI Framework**: Tkinter (standard library)
- **Database**: SQLite via Python sqlite3 module
- **Dependencies**: Pillow, Pandas, Matplotlib, Seaborn, Plotly, PyWebView

### Architecture

- Layered architecture with clear separation of concerns
- GUI layer (Tkinter UI)
- Business logic layer (Analysis, Config, Utils)
- Data persistence layer (SQLite + CSV legacy support)

---

## Future Releases

### [Unreleased]

#### Planned Features

- Custom user-defined expense categories
- Date range filtering for expense viewing
- Recurring expense automation
- Budget tracking and alerts
- Monthly summary reports
- Search and filter functionality
- Multi-currency support
- Cloud sync capabilities
- Enhanced export options (PDF, Excel)
- Bank statement import
- Receipt scanning (OCR)

---

## Version History

- **1.0.0** (2026-01-07) - Initial public release

---

## How to Update

### For Users

When a new version is released:

1. **Check the changelog** for new features and breaking changes
2. **Backup your data** using the built-in backup feature
3. **Pull the latest changes**:
   ```bash
   git pull origin main
   ```
4. **Update dependencies**:
   ```bash
   pip install -r requirements.txt --upgrade
   ```
5. **Run migrations** if needed (instructions will be in release notes)
6. **Test the application** to ensure everything works

### For Developers

When contributing:

1. **Read the changelog** to understand recent changes
2. **Update the changelog** when adding new features
3. **Follow semantic versioning** for version numbers
4. **Document breaking changes** clearly
5. **Add migration guides** for database schema changes

---

## Semantic Versioning

This project uses [Semantic Versioning](https://semver.org/):

- **MAJOR** version (X.0.0): Incompatible API changes
- **MINOR** version (0.X.0): New functionality (backward-compatible)
- **PATCH** version (0.0.X): Bug fixes (backward-compatible)

---

## Release Process

1. Update version number in relevant files
2. Update this CHANGELOG.md
3. Update RELEASE_NOTES.md with user-facing changes
4. Run full test suite: `pytest -v`
5. Build executable: `pyinstaller --clean --noconfirm gui_expense_tracker.spec`
6. Create git tag: `git tag -a v1.0.0 -m "Release version 1.0.0"`
7. Push tag: `git push origin v1.0.0`
8. Create GitHub release with artifacts

---

## Notes

- See [RELEASE_NOTES.md](RELEASE_NOTES.md) for user-friendly release information
- See [REFACTORING_SUMMARY.md](REFACTORING_SUMMARY.md) for refactoring history
- See [DEVELOPER_GUIDELINES.md](DEVELOPER_GUIDELINES.md) for development practices

---

**For questions or issues, please open an issue on GitHub.**
