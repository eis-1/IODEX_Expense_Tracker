# Developer Guidelines

This document contains practical, human-oriented guidance for contributors and maintainers of the project. It replaces earlier, tool-specific instructions and focuses on repeatable developer workflows, testing, and reviewability.

## Purpose

Keep contributions small, well-tested, and easy to review. Prefer changes to non-UI modules (`storage.py`, `analysis.py`, `utils.py`) where possible and extract logic from GUI code (`gui.py`) so it can be unit tested.

## Quick commands

```powershell
# create venv
python -m venv .venv
& ".venv/Scripts/Activate.ps1"
pip install -r requirements.txt

# run app
python gui_expense_tracker.py

# run tests
python -m pytest -q

# lint
python -m ruff check .
```

## Testing

- Add unit tests for business logic and storage using `tmp_path` or `path=` arguments to avoid mutating production data.
- GUI behavior should be kept minimal in tests — test logic via helpers (e.g., preview/formatting functions) instead.

## Review and PRs

- Open a small PR that explains the behavior change, includes tests, and cites any migration steps.
- Run the full test suite locally before requesting review and include test results in the PR description.

## Automation & CI

- CI should run linting, type checks, and the test suite. Keep CI configuration minimal and deterministic.
- Don't rely on environment-specific tools in CI unless they are installed by the workflow (document any extra setup).

## Notes for maintainers

- Use descriptive commit messages and squash/fixup small work-in-progress commits before finalizing a PR.
- For large refactors, open an issue first to discuss design and migration strategy.

---

If you'd like this file placed at the repository root instead of `.github/`, or want me to include a short contributor checklist, say which and I will update it.
