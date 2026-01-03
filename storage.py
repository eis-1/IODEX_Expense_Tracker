"""
Storage module for expense data persistence.
Handles reading, writing, and clearing expense records using CSV format.
"""
import csv
import os

DEFAULT_FILENAME = "expenses.txt"


from datetime import datetime, timezone

def append_expense(category: str, amount: float, description: str, path: str = DEFAULT_FILENAME, timestamp: str | None = None) -> None:
    """
    Append a single expense record to the storage file.

    Args:
        category: Expense category (e.g., 'Food', 'Rent')
        amount: Numeric amount of the expense
        description: Optional description of the expense
        path: File path for storage (defaults to expenses.txt)
        timestamp: ISO-format timestamp string to record (optional)

    Raises:
        ValueError: If category/amount are empty or amount is not numeric
        IOError: If file cannot be written
    """
    if not category:
        raise ValueError("Category and Amount are required.")

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        raise ValueError("Amount must be a number.")

    if amount < 0:
        raise ValueError("Amount cannot be negative.")

    if timestamp is None:
        timestamp = datetime.now(timezone.utc).isoformat()

    with open(path, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([category, amount, description, timestamp])


def load_expenses(path: str = DEFAULT_FILENAME) -> list:
    """
    Load all expense records from the storage file.

    Args:
        path: File path to read from (defaults to expenses.txt)

    Returns:
        List of tuples: [(category, amount, description, timestamp), ...]
        Returns empty list if file doesn't exist.
        Skips malformed rows.

    Raises:
        IOError: If file cannot be read
    """
    if not os.path.exists(path):
        return []

    expenses = []
    with open(path, "r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row_num, parts in enumerate(reader, start=1):
            if len(parts) >= 3:
                try:
                    # Validate amount is numeric
                    amount = float(parts[1])
                    if amount < 0:
                        # Skip rows with negative amounts
                        continue
                    description = parts[2]
                    timestamp = parts[3] if len(parts) >= 4 else None
                    expenses.append((parts[0], amount, description, timestamp))
                except (ValueError, IndexError):
                    # Skip rows with invalid amounts
                    continue

    return expenses


def get_total_spent(path: str = DEFAULT_FILENAME) -> float:
    """
    Calculate total amount spent across all expenses.
    
    Args:
        path: File path to read from (defaults to expenses.txt)
    
    Returns:
        Total amount as float. Returns 0.0 if no expenses exist.
    """
    expenses = load_expenses(path)
    return sum(exp[1] for exp in expenses)


def clear_expenses(path: str = DEFAULT_FILENAME) -> None:
    """
    Delete all expense records from storage.
    
    Args:
        path: File path to clear (defaults to expenses.txt)
    
    Raises:
        IOError: If file cannot be written
    """
    with open(path, "w", newline="", encoding="utf-8") as file:
        file.truncate()


def file_exists(path: str = DEFAULT_FILENAME) -> bool:
    """
    Check if the expense storage file exists.

    Args:
        path: File path to check (defaults to expenses.txt)

    Returns:
        True if expense file exists, False otherwise
    """
    return os.path.exists(path)


def delete_expense(category: str, amount: float, description: str, timestamp: str | None = None, path: str = DEFAULT_FILENAME) -> bool:
    """Delete the first matching expense from the CSV storage.

    Matching is done by exact category, amount (numeric), description, and optional timestamp.
    Returns True if a row was deleted, False otherwise.
    """
    if not os.path.exists(path):
        return False

    deleted = False
    rows = []
    with open(path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for parts in reader:
            if len(parts) < 3:
                rows.append(parts)
                continue
            cat = parts[0]
            try:
                amt = float(parts[1])
            except Exception:
                rows.append(parts)
                continue
            desc = parts[2]
            ts = parts[3] if len(parts) >= 4 else None

            if (not deleted and cat == category and abs(amt - float(amount)) < 1e-6 and desc == description and (timestamp is None or ts == timestamp)):
                deleted = True
                continue  # skip this row (delete)
            rows.append(parts)

    if deleted:
        # Write back remaining rows
        dirpath = os.path.dirname(path)
        if dirpath and not os.path.exists(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        with open(path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for r in rows:
                writer.writerow(r)
    return deleted
