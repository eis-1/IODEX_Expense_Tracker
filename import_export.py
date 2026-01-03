"""
Import/Export module for expense data.
Supports CSV and JSON formats for data portability.
"""
import csv
import json
import os
from datetime import datetime, timezone
from typing import List, Tuple

from database import ExpenseDatabase


class ImportExporter:
    """Handles importing and exporting expense data."""
    
    @staticmethod
    def export_to_csv(db: ExpenseDatabase, filepath: str) -> None:
        """
        Export all expenses to CSV file.
        
        Args:
            db: ExpenseDatabase instance
            filepath: Path to save CSV file
            
        Raises:
            IOError: If file cannot be written
        """
        expenses = db.load_expenses()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Write header
            writer.writerow(['ID', 'Category', 'Amount', 'Description', 'Timestamp'])
            # Write data
            for expense in expenses:
                writer.writerow(expense)
    
    @staticmethod
    def export_to_json(db: ExpenseDatabase, filepath: str) -> None:
        """
        Export all expenses to JSON file.
        
        Args:
            db: ExpenseDatabase instance
            filepath: Path to save JSON file
            
        Raises:
            IOError: If file cannot be written
        """
        expenses = db.load_expenses()
        
        data = {
            'export_date': datetime.now(timezone.utc).isoformat(),
            'total_records': len(expenses),
            'expenses': [
                {
                    'id': exp[0],
                    'category': exp[1],
                    'amount': exp[2],
                    'description': exp[3],
                    'timestamp': exp[4]
                }
                for exp in expenses
            ]
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def import_from_csv(db: ExpenseDatabase, filepath: str) -> int:
        """
        Import expenses from CSV file.
        
        CSV should have columns: Category, Amount, Description (ID and Timestamp are auto-generated)
        
        Args:
            db: ExpenseDatabase instance
            filepath: Path to CSV file
            
        Returns:
            Number of records imported
            
        Raises:
            IOError: If file cannot be read
            ValueError: If data format is invalid
        """
        imported_count = 0
        
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            # Check for required columns
            if reader.fieldnames is None:
                raise ValueError("CSV file is empty")
            
            required_cols = {'Category', 'Amount', 'Description'}
            csv_cols = set(reader.fieldnames)
            
            # Be flexible with column names
            if not any(col in csv_cols for col in ['Category', 'category']):
                raise ValueError("CSV must contain 'Category' column")
            if not any(col in csv_cols for col in ['Amount', 'amount']):
                raise ValueError("CSV must contain 'Amount' column")
            
            for row_num, row in enumerate(reader, start=2):  # Start at 2 (after header)
                try:
                    # Get values with flexible column names
                    category = row.get('Category') or row.get('category', '').strip()
                    amount_str = row.get('Amount') or row.get('amount', '').strip()
                    description = row.get('Description') or row.get('description', '').strip()
                    
                    if not category or not amount_str:
                        continue  # Skip empty rows
                    
                    db.append_expense(category, float(amount_str), description)
                    imported_count += 1
                
                except (ValueError, KeyError) as e:
                    # Skip malformed rows, continue importing
                    continue
        
        return imported_count
    
    @staticmethod
    def import_from_json(db: ExpenseDatabase, filepath: str) -> int:
        """
        Import expenses from JSON file.
        
        Args:
            db: ExpenseDatabase instance
            filepath: Path to JSON file
            
        Returns:
            Number of records imported
            
        Raises:
            IOError: If file cannot be read
            ValueError: If data format is invalid
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if not isinstance(data, dict):
            raise ValueError("JSON must be an object")
        
        if 'expenses' not in data:
            raise ValueError("JSON must contain 'expenses' array")
        
        expenses = data['expenses']
        if not isinstance(expenses, list):
            raise ValueError("'expenses' must be an array")
        
        imported_count = 0
        for expense in expenses:
            try:
                category = str(expense.get('category', '')).strip()
                amount_str = str(expense.get('amount', '')).strip()
                description = str(expense.get('description', '')).strip()
                
                if not category or not amount_str:
                    continue  # Skip incomplete entries
                
                db.append_expense(category, float(amount_str), description)
                imported_count += 1
            
            except (ValueError, TypeError, AttributeError):
                # Skip malformed entries, continue importing
                continue
        
        return imported_count
    
    @staticmethod
    def detect_format(filepath: str) -> str:
        """
        Detect file format based on extension.
        
        Args:
            filepath: Path to file
            
        Returns:
            'csv', 'json', or 'unknown'
        """
        ext = os.path.splitext(filepath)[1].lower()
        if ext == '.csv':
            return 'csv'
        elif ext == '.json':
            return 'json'
        return 'unknown'
