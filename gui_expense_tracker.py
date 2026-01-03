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

from gui import run_application

if __name__ == "__main__":
    run_application()