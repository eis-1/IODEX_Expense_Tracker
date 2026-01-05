Contributing to GUI Expense Tracker

Thank you for your interest in contributing! Please follow these simple guidelines to make the project easy to review and maintain.

1. Fork the repository and create a feature branch

   - Branch name format: `feature/short-description` or `fix/short-description`

2. Development setup
   - Create a virtual environment and install requirements:

```powershell
python -m venv .venv
& ".venv/Scripts/Activate.ps1"
python -m pip install -r requirements.txt
```

3. Code style and checks
   - Run the linter and type checker before committing:

```powershell
python -m ruff check .
python -m mypy .   # optional if installed
```

4. Tests
   - Add tests for new features or bug fixes. Run the test suite locally:

```powershell
python -m pytest -q
```

5. Commit messages and PRs

   - Keep commits small and focused. Use present-tense messages (e.g., "Fix parsing bug").
   - Open a pull request against `main` with a clear description, rationale, and test coverage.

6. Code of Conduct

   - Be respectful and follow standard community etiquette. If you'd like, we can add a formal `CODE_OF_CONDUCT.md`.

7. Questions
   - Open an issue to discuss large changes before implementing them.

Thanks — maintainers will review pull requests and provide feedback.
