# Quick Start Guide

Get up and running with GUI Expense Tracker in 5 minutes!

## 🚀 For Users

### Windows

```powershell
# 1. Download the executable (if available)
# Download gui_expense_tracker.exe from releases

# 2. Run the application
.\gui_expense_tracker.exe
```

### From Source

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/gui-expense-tracker.git
cd gui-expense-tracker

# 2. Install Python 3.10+ if needed
# Download from: https://www.python.org/downloads/

# 3. Create virtual environment
python -m venv .venv

# 4. Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Run the application
python gui_expense_tracker.py
```

## 👨‍💻 For Developers

### First-Time Setup

```bash
# 1. Fork the repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/gui-expense-tracker.git
cd gui-expense-tracker

# 3. Add upstream remote
git remote add upstream https://github.com/ORIGINAL_OWNER/gui-expense-tracker.git

# 4. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\Activate.ps1

# 5. Install dependencies
pip install -r requirements.txt

# 6. Install development tools
pip install pytest pytest-cov mypy ruff

# 7. Run tests to verify setup
pytest -v

# 8. Start developing!
```

### Daily Workflow

```bash
# 1. Update your local repository
git fetch upstream
git checkout main
git merge upstream/main

# 2. Create a feature branch
git checkout -b feature/my-awesome-feature

# 3. Make your changes
# Edit files, add features, fix bugs

# 4. Run tests
pytest -v

# 5. Check code quality
ruff check .
mypy .

# 6. Commit your changes
git add .
git commit -m "Add awesome feature"

# 7. Push to your fork
git push origin feature/my-awesome-feature

# 8. Open a Pull Request on GitHub
```

## 🧪 Running Tests

```bash
# All tests
pytest

# Verbose output
pytest -v

# Specific test file
pytest test_storage.py -v

# With coverage report
pytest --cov=. --cov-report=html
# Open htmlcov/index.html in browser

# Watch mode (requires pytest-watch)
pip install pytest-watch
ptw
```

## 🔧 Common Tasks

### Add a New Feature

```bash
git checkout -b feature/my-feature
# Make changes
pytest -v
git commit -am "Add my feature"
git push origin feature/my-feature
# Open PR
```

### Fix a Bug

```bash
git checkout -b fix/issue-123
# Make changes
pytest -v
git commit -am "Fix issue #123"
git push origin fix/issue-123
# Open PR
```

### Update Dependencies

```bash
pip install --upgrade -r requirements.txt
pip freeze > requirements.txt
git commit -am "Update dependencies"
```

### Build Executable

```powershell
# Windows
pip install pyinstaller
pyinstaller --clean --noconfirm gui_expense_tracker.spec
# Output in dist/gui_expense_tracker.exe

# Or use the build script
.\build_exe.ps1
```

## 📖 Key Files

| File                      | Purpose                 |
| ------------------------- | ----------------------- |
| `README.md`               | Project overview        |
| `CONTRIBUTING.md`         | Contribution guidelines |
| `DEVELOPER_GUIDELINES.md` | Development practices   |
| `TESTING_GUIDE.md`        | Testing documentation   |
| `requirements.txt`        | Python dependencies     |

## 🆘 Troubleshooting

### "No module named 'tkinter'"

```bash
# Ubuntu/Debian
sudo apt-get install python3-tk

# macOS
brew install python-tk

# Windows - Reinstall Python with Tk support
```

### "pytest not found"

```bash
# Use python -m prefix
python -m pytest -v

# Or install pytest
pip install pytest
```

### Virtual Environment Issues

```bash
# Deactivate current environment
deactivate

# Remove old environment
rm -rf .venv  # or rmdir /s .venv on Windows

# Create fresh environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Import Errors

```bash
# Ensure virtual environment is activated
# You should see (.venv) in your prompt

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list
```

## 💡 Tips

- **Always use virtual environment** - Keeps dependencies isolated
- **Run tests before committing** - Catches issues early
- **Write descriptive commit messages** - Helps with code review
- **Keep commits atomic** - One logical change per commit
- **Update documentation** - When adding features
- **Ask questions** - Open an issue if stuck

## 🔗 Useful Links

- [Python Documentation](https://docs.python.org/3/)
- [Tkinter Tutorial](https://docs.python.org/3/library/tkinter.html)
- [pytest Documentation](https://docs.pytest.org/)
- [Git Basics](https://git-scm.com/book/en/v2/Getting-Started-Git-Basics)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

## 📞 Get Help

- **Documentation**: Check the docs in the repository
- **Issues**: Search existing issues or create a new one
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact the maintainer (see README)

---

**Happy Coding! 🎉**
