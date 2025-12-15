# IODEX — Super Duper Expense Tracker

A simple, friendly desktop GUI for tracking personal expenses, built with Python and Tkinter. Add expenses, view them in a table, and analyze totals by category with an in-app bar chart.

## Quick Start

- **Requirements:** Python 3.10+
- **Install dependencies:**

```bash
pip install -r requirements.txt
```

- **Run the app:**

```bash
python gui_expense_tracker.py
```

## Features

- **Add Expense:** Save category, amount, and optional description.
- **View All:** Browse every expense in a table and see the total spent.
- **Analyze:** In-app bar chart showing total spent per category (uses pandas + seaborn).
- **Reset:** Wipe all recorded expenses.

## Files

- `gui_expense_tracker.py`: Main GUI program. Launch this to use the tracker.
- `expenses.txt`: Plain-text data file where each line is `Category,Amount,Description`.
- `requirements.txt`: Python dependencies (`pillow`, `pandas`, `matplotlib`, `seaborn`).

Notes:

- The app will create `expenses.txt` in the working directory if it doesn't exist.
- If you want a background image in the GUI, place `photo1.jpg` next to `gui_expense_tracker.py`.

## Usage Tips

- Enter numeric amounts (e.g., `12.50`). Non-numeric input will be rejected.
- If the app reports "No Data" for analysis or view, add at least one expense first.

## Troubleshooting

- Missing module errors: run `pip install -r requirements.txt`.
- Background image errors are non-fatal — the app falls back to a plain background.

## Author

Created by MD EAFTEKHIRUL ISLAM 

## License

This project is provided without an explicit license. Add a LICENSE file if you want to set usage terms.
