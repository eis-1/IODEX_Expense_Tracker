"""
Storage module for expense data persistence.
Supports both legacy CSV files and a modern SQLite backend.
Functions keep the original CSV signatures so the GUI remains compatible.
"""

import csv
import sqlite3
import os
from datetime import datetime, timezone
from typing import List, Tuple

DEFAULT_FILENAME = "expenses.db"


def _is_sqlite_file(path: str) -> bool:
    """Return True if the file at `path` is a SQLite database or the path looks like one.

    Heuristics:
    - If the path ends with `.db` treat as SQLite.
    - If the file exists and its header matches the SQLite magic header, treat as SQLite.
    """
    if path.lower().endswith(".db"):
        return True
    if not os.path.exists(path):
        return False
    try:
        with open(path, "rb") as f:
            header = f.read(16)
            return header == b"SQLite format 3\x00"
    except Exception:
        return False


def _get_connection(path: str = DEFAULT_FILENAME) -> sqlite3.Connection:
    """Open (or create) an SQLite connection and ensure the schema exists."""
    dirpath = os.path.dirname(path) if os.path.dirname(path) else "."
    if dirpath and not os.path.exists(dirpath):
        os.makedirs(dirpath, exist_ok=True)
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount >= 0),
            description TEXT DEFAULT '',
            timestamp TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn


def append_expense(
    category: str,
    amount: float,
    description: str,
    path: str = DEFAULT_FILENAME,
    timestamp: str | None = None,
) -> None:
    """
    Append a single expense record to the database.

    Args:
        category: Expense category (e.g., 'Food', 'Rent')
        amount: Numeric amount of the expense
        description: Optional description of the expense
        path: Database file path (defaults to expenses.db)
        timestamp: ISO-format timestamp string to record (optional)

    Raises:
        ValueError: If category/amount are empty or amount is not numeric
        sqlite3.Error: If database operation fails
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

    # If the path looks like a sqlite DB, use the DB backend; otherwise keep CSV behaviour
    if _is_sqlite_file(path):
        try:
            conn = _get_connection(path)
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO expenses (category, amount, description, timestamp) VALUES (?, ?, ?, ?)",
                (category, amount, description, timestamp),
            )
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            raise IOError(f"Failed to append expense to database: {str(e)}")
    else:
        # Legacy CSV append (preserve previous behaviour)
        try:
            dirpath = os.path.dirname(path)
            if dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            with open(path, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow([category, amount, description, timestamp])
        except Exception as e:
            raise IOError(f"Failed to append expense to CSV file: {str(e)}")


def load_expenses(path: str = DEFAULT_FILENAME) -> List[Tuple[str, float, str, str]]:
    """
    Load all expense records from the database.

    Args:
        path: Database file path (defaults to expenses.db)

    Returns:
        List of tuples: [(category, amount, description, timestamp), ...]
        Returns empty list if database doesn't exist or has no expenses.
        Tuples maintain the same format as the CSV predecessor for GUI compatibility.

    Raises:
        IOError: If database cannot be read
    """
    if not os.path.exists(path):
        return []

    # Database mode
    if _is_sqlite_file(path):
        try:
            conn = _get_connection(path)
            cursor = conn.cursor()
            # Preserve append order (id asc) to match CSV ordering in tests/gui
            cursor.execute(
                "SELECT category, amount, description, timestamp FROM expenses ORDER BY id ASC"
            )
            rows = cursor.fetchall()
            conn.close()
            expenses = []
            for category, amount, description, timestamp in rows:
                # filter negative amounts just in case
                if amount is None:
                    continue
                try:
                    amt = float(amount)
                except Exception:
                    continue
                if amt >= 0:
                    expenses.append((category, amt, description, timestamp))
            return expenses
        except sqlite3.Error as e:
            raise IOError(f"Failed to load expenses from database: {str(e)}")

    # Legacy CSV mode
    expenses = []
    try:
        with open(path, "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            for parts in reader:
                if len(parts) >= 3:
                    try:
                        amount = float(parts[1])
                        if amount < 0:
                            continue
                        description = parts[2]
                        timestamp = parts[3] if len(parts) >= 4 else None
                        expenses.append((parts[0], amount, description, timestamp))
                    except (ValueError, IndexError):
                        continue
    except FileNotFoundError:
        return []
    return expenses


def get_total_spent(path: str = DEFAULT_FILENAME) -> float:
    """
    Calculate total amount spent across all expenses.

    Args:
        path: Database file path (defaults to expenses.db)

    Returns:
        Total amount as float. Returns 0.0 if no expenses exist.
    """
    # DB mode: use SQL SUM for efficiency
    if _is_sqlite_file(path):
        try:
            conn = _get_connection(path)
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(amount) FROM expenses")
            res = cursor.fetchone()
            conn.close()
            total = res[0] if res and res[0] is not None else 0.0
            return float(total)
        except Exception:
            return 0.0
    # CSV fallback
    try:
        expenses = load_expenses(path)
        return sum(exp[1] for exp in expenses)
    except Exception:
        return 0.0


def clear_expenses(path: str = DEFAULT_FILENAME) -> None:
    """
    Delete all expense records from storage (DB or CSV depending on path).
    """
    # DB mode
    if _is_sqlite_file(path):
        try:
            conn = _get_connection(path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses")
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            raise IOError(f"Failed to clear expenses from database: {str(e)}")
    else:
        # CSV mode: truncate file
        try:
            dirpath = os.path.dirname(path)
            if dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            with open(path, "w", newline="", encoding="utf-8") as file:
                file.truncate()
        except Exception as e:
            raise IOError(f"Failed to clear CSV expenses file: {str(e)}")


def file_exists(path: str = DEFAULT_FILENAME) -> bool:
    """
    Check if the expense storage exists. For DB-like paths, verify schema; otherwise check file existence.
    """
    if _is_sqlite_file(path):
        if not os.path.exists(path):
            return False
        try:
            conn = sqlite3.connect(path)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='expenses'"
            )
            result = cursor.fetchone()
            conn.close()
            return result is not None
        except sqlite3.Error:
            return False
    return os.path.exists(path)


def delete_expense(
    category: str,
    amount: float,
    description: str,
    timestamp: str | None = None,
    path: str = DEFAULT_FILENAME,
) -> bool:
    """
    Delete the first matching expense. Supports both CSV and SQLite files.
    Matching by category, numeric amount (tolerance), description, and optional timestamp.
    """
    # CSV mode
    if not _is_sqlite_file(path):
        if not os.path.exists(path):
            return False
        deleted = False
        rows = []
        try:
            with open(path, "r", newline="", encoding="utf-8") as f:
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

                    if (
                        not deleted
                        and cat == category
                        and abs(amt - float(amount)) < 1e-6
                        and desc == description
                        and (timestamp is None or ts == timestamp)
                    ):
                        deleted = True
                        continue
                    rows.append(parts)
        except FileNotFoundError:
            return False

        if deleted:
            dirpath = os.path.dirname(path)
            if dirpath and not os.path.exists(dirpath):
                os.makedirs(dirpath, exist_ok=True)
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for r in rows:
                    writer.writerow(r)
        return deleted

    # DB mode
    try:
        if not os.path.exists(path):
            return False
        conn = _get_connection(path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, amount, timestamp FROM expenses WHERE category = ? AND description = ? ORDER BY id ASC",
            (category, description),
        )
        candidates = cursor.fetchall()
        target_id = None
        for cid, amt, ts in candidates:
            try:
                if abs(float(amt) - float(amount)) < 1e-6 and (
                    timestamp is None or ts == timestamp
                ):
                    target_id = cid
                    break
            except Exception:
                continue
        if target_id is not None:
            cursor.execute("DELETE FROM expenses WHERE id = ?", (target_id,))
            conn.commit()
            conn.close()
            return True
        conn.close()
        return False
    except sqlite3.Error as e:
        raise IOError(f"Failed to delete expense from database: {str(e)}")
