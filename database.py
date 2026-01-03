"""
Database module for SQLite expense storage.
Provides robust local database with atomic transactions and schema management.
"""
import sqlite3
import os
from datetime import datetime
from typing import List, Tuple, Optional

DEFAULT_DB_PATH = "expenses.db"


class ExpenseDatabase:
    """SQLite database manager for expense tracking."""
    
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        """
        Initialize database connection and create schema if needed.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Create database schema if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS expenses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount >= 0),
                    description TEXT DEFAULT '',
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
    
    def append_expense(self, category: str, amount: float, description: str) -> int:
        """
        Add a new expense record to the database.
        
        Args:
            category: Expense category
            amount: Expense amount (must be non-negative)
            description: Optional description
            
        Returns:
            ID of inserted record
            
        Raises:
            ValueError: If inputs are invalid
            sqlite3.Error: If database operation fails
        """
        if not category:
            raise ValueError("Category is required.")
        
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ValueError("Amount must be a number.")
        
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO expenses (category, amount, description)
                VALUES (?, ?, ?)
            """, (category, amount, description))
            conn.commit()
            return cursor.lastrowid
    
    def load_expenses(self) -> List[Tuple[int, str, float, str, str]]:
        """
        Load all expense records from database.
        
        Returns:
            List of tuples: [(id, category, amount, description, timestamp), ...]
            Returns empty list if no expenses exist.
        """
        if not os.path.exists(self.db_path):
            return []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, category, amount, description, timestamp
                FROM expenses
                ORDER BY timestamp DESC
            """)
            return cursor.fetchall()
    
    def load_expenses_by_category(self, category: str) -> List[Tuple[int, str, float, str, str]]:
        """
        Load expenses for a specific category.
        
        Args:
            category: Category to filter by
            
        Returns:
            List of expense tuples for the category
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, category, amount, description, timestamp
                FROM expenses
                WHERE category = ?
                ORDER BY timestamp DESC
            """, (category,))
            return cursor.fetchall()
    
    def get_total_spent(self) -> float:
        """
        Calculate total amount spent across all expenses.
        
        Returns:
            Total amount as float. Returns 0.0 if no expenses exist.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT SUM(amount) FROM expenses")
            result = cursor.fetchone()
            return result[0] if result[0] is not None else 0.0
    
    def get_category_totals(self) -> dict:
        """
        Get total spending per category.
        
        Returns:
            Dictionary with category names as keys and totals as values
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT category, SUM(amount) as total
                FROM expenses
                GROUP BY category
                ORDER BY total DESC
            """)
            return {row[0]: row[1] for row in cursor.fetchall()}
    
    def delete_expense(self, expense_id: int) -> bool:
        """
        Delete a specific expense by ID.
        
        Args:
            expense_id: ID of expense to delete
            
        Returns:
            True if expense was deleted, False if not found
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
            conn.commit()
            return cursor.rowcount > 0
    
    def update_expense(self, expense_id: int, category: str, amount: float, 
                      description: str) -> bool:
        """
        Update an existing expense record.
        
        Args:
            expense_id: ID of expense to update
            category: New category
            amount: New amount
            description: New description
            
        Returns:
            True if expense was updated, False if not found
            
        Raises:
            ValueError: If inputs are invalid
        """
        if not category:
            raise ValueError("Category is required.")
        
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ValueError("Amount must be a number.")
        
        if amount < 0:
            raise ValueError("Amount cannot be negative.")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE expenses
                SET category = ?, amount = ?, description = ?
                WHERE id = ?
            """, (category, amount, description, expense_id))
            conn.commit()
            return cursor.rowcount > 0
    
    def clear_expenses(self) -> None:
        """Delete all expense records from database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM expenses")
            conn.commit()
    
    def get_database_size(self) -> int:
        """
        Get database file size in bytes.
        
        Returns:
            File size in bytes
        """
        if os.path.exists(self.db_path):
            return os.path.getsize(self.db_path)
        return 0
    
    def vacuum(self) -> None:
        """Optimize database by removing unused space."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("VACUUM")
    
    def get_statistics(self) -> dict:
        """
        Get summary statistics about expenses.
        
        Returns:
            Dictionary with keys: count, total, average, min, max, by_category
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT 
                    COUNT(*) as count,
                    SUM(amount) as total,
                    AVG(amount) as average,
                    MIN(amount) as min_amount,
                    MAX(amount) as max_amount
                FROM expenses
            """)
            stats = cursor.fetchone()
            
            return {
                'count': stats[0] or 0,
                'total': stats[1] or 0.0,
                'average': stats[2] or 0.0,
                'min': stats[3] or 0.0,
                'max': stats[4] or 0.0,
                'by_category': self.get_category_totals()
            }
    
    def file_exists(self) -> bool:
        """
        Check if database file exists.
        
        Returns:
            True if database file exists
        """
        return os.path.exists(self.db_path)
