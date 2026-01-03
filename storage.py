"""
Storage module for expense data persistence.
Handles reading, writing, and clearing expense records using CSV format.
"""
import csv
import os

DEFAULT_FILENAME = "expenses.txt"


def append_expense(category: str, amount: float, description: str, path: str = DEFAULT_FILENAME) -> None:
    """
    Append a single expense record to the storage file.
    
    Args:
        category: Expense category (e.g., 'Food', 'Rent')
        amount: Numeric amount of the expense
        description: Optional description of the expense
        path: File path for storage (defaults to expenses.txt)
        
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
    
    with open(path, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([category, amount, description])


def load_expenses(path: str = DEFAULT_FILENAME) -> list:
    """
    Load all expense records from the storage file.
    
    Args:
        path: File path to read from (defaults to expenses.txt)
    
    Returns:
        List of tuples: [(category, amount, description), ...]
        Returns empty list if file doesn't exist.
        Skips malformed rows.
        
    Raises:
        IOError: If file cannot be read
    """
    if not os.path.exists(path):
        return []
    
    expenses = []
    with open(path, "r", newline="") as file:
        reader = csv.reader(file)
        for row_num, parts in enumerate(reader, start=1):
            if len(parts) >= 3:
                try:
                    # Validate amount is numeric
                    amount = float(parts[1])
                    if amount < 0:
                        # Skip rows with negative amounts
                        continue
                    expenses.append((parts[0], amount, parts[2]))
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
    return sum(amount for _, amount, _ in expenses)


def clear_expenses(path: str = DEFAULT_FILENAME) -> None:
    """
    Delete all expense records from storage.
    
    Args:
        path: File path to clear (defaults to expenses.txt)
    
    Raises:
        IOError: If file cannot be written
    """
    with open(path, "w", newline="") as file:
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
