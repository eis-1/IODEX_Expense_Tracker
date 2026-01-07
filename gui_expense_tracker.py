"""
IODEX Expense Tracker - Main Entry Point

A compact desktop expense-tracking application implemented with Python and Tkinter.
The program records expense entries with proper CSV handling, provides a view of saved records,
and offers category-based analysis with charts.

Modules:
    - storage.py: File I/O and data persistence
    - gui.py: User interface and interaction
    - analysis.py: Data visualization and aggregation
"""

import logging
import os
from pathlib import Path

from gui import run_application


def _setup_logging() -> None:
    """Configure basic logging for production runs.

    - Writes to a user-writable location (AppData on Windows).
    - Keeps console logging for dev runs.
    """
    appdata = os.getenv("APPDATA")
    base_dir = Path(appdata) if appdata else Path.home()
    log_dir = base_dir / "IODEX_Expense_Tracker" / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "app.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


if __name__ == "__main__":
    _setup_logging()
    run_application()
