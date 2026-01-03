"""
Unit tests for database, import/export, and backup modules.
Tests SQLite functionality, data migration, and file operations.

Run with: pytest test_database.py -v
"""
import pytest
import os
import tempfile
import json
import sqlite3
from database import ExpenseDatabase
from import_export import ImportExporter
from backup import BackupManager


@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    os.remove(path)  # Remove empty file, let DB create it
    yield path
    # Cleanup
    # Avoid removing the temporary DB file on Windows to prevent PermissionError
    # The OS or other process may hold locks; leaving the file is acceptable for CI/local tests.
    pass


@pytest.fixture
def temp_dir():
    """Create a temporary directory for testing."""
    path = tempfile.mkdtemp()
    yield path
    # Cleanup
    import shutil, time, sqlite3
    if os.path.exists(path):
        # Try to close any sqlite DB files in the directory to release locks
        for root, _, files in os.walk(path):
            for name in files:
                if name.endswith('.db'):
                    dbfile = os.path.join(root, name)
                    try:
                        conn = sqlite3.connect(dbfile)
                        conn.close()
                    except Exception:
                        pass
        # Attempt removal with retries to handle transient locks
        for _ in range(5):
            try:
                shutil.rmtree(path)
                break
            except PermissionError:
                time.sleep(0.1)


class TestExpenseDatabase:
    """Tests for ExpenseDatabase class."""
    
    def test_database_creation(self, temp_db):
        """Test database is created with proper schema."""
        db = ExpenseDatabase(temp_db)
        assert os.path.exists(temp_db)
        assert db.file_exists()
    
    def test_append_valid_expense(self, temp_db):
        """Test appending a valid expense."""
        db = ExpenseDatabase(temp_db)
        expense_id = db.append_expense("Food", 10.50, "Lunch")
        assert expense_id > 0
        assert db.get_total_spent() == 10.50
    
    def test_append_multiple_expenses(self, temp_db):
        """Test appending multiple expenses."""
        db = ExpenseDatabase(temp_db)
        id1 = db.append_expense("Food", 10.00, "Breakfast")
        id2 = db.append_expense("Rent", 500.00, "Monthly")
        id3 = db.append_expense("Utilities", 50.00, "Electric")
        
        assert id1 != id2 != id3
        assert db.get_total_spent() == 560.00
    
    def test_load_expenses(self, temp_db):
        """Test loading expenses from database."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 15.00, "Lunch")
        db.append_expense("Transport", 5.00, "Bus")
        
        expenses = db.load_expenses()
        assert len(expenses) == 2
        # Ensure both categories are present (order may vary by timestamp precision)
        categories = [exp[1] for exp in expenses]
        assert "Food" in categories
        assert "Transport" in categories
    
    def test_get_total_spent(self, temp_db):
        """Test total calculation."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 10.00, "")
        db.append_expense("Rent", 500.00, "")
        db.append_expense("Utilities", 50.00, "")
        
        assert db.get_total_spent() == 560.00
    
    def test_get_category_totals(self, temp_db):
        """Test category aggregation."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 10.00, "")
        db.append_expense("Food", 15.00, "")
        db.append_expense("Rent", 500.00, "")
        
        totals = db.get_category_totals()
        assert totals["Food"] == 25.00
        assert totals["Rent"] == 500.00
    
    def test_invalid_amount_non_numeric(self, temp_db):
        """Test that non-numeric amounts raise ValueError."""
        db = ExpenseDatabase(temp_db)
        with pytest.raises(ValueError, match="Amount must be a number"):
            db.append_expense("Food", "abc", "Lunch")
    
    def test_invalid_amount_negative(self, temp_db):
        """Test that negative amounts raise ValueError."""
        db = ExpenseDatabase(temp_db)
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            db.append_expense("Food", -10.00, "Lunch")
    
    def test_missing_category(self, temp_db):
        """Test that missing category raises ValueError."""
        db = ExpenseDatabase(temp_db)
        with pytest.raises(ValueError, match="Category is required"):
            db.append_expense("", 10.00, "Lunch")
    
    def test_delete_expense(self, temp_db):
        """Test deleting an expense."""
        db = ExpenseDatabase(temp_db)
        id1 = db.append_expense("Food", 10.00, "")
        id2 = db.append_expense("Rent", 500.00, "")
        
        deleted = db.delete_expense(id1)
        assert deleted
        assert db.get_total_spent() == 500.00
    
    def test_update_expense(self, temp_db):
        """Test updating an expense."""
        db = ExpenseDatabase(temp_db)
        expense_id = db.append_expense("Food", 10.00, "Lunch")
        
        updated = db.update_expense(expense_id, "Dining", 15.00, "Dinner")
        assert updated
        
        expenses = db.load_expenses()
        assert expenses[0][1] == "Dining"
        assert expenses[0][2] == 15.00
    
    def test_clear_expenses(self, temp_db):
        """Test clearing all expenses."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 10.00, "")
        db.append_expense("Rent", 500.00, "")
        
        db.clear_expenses()
        assert db.get_total_spent() == 0.0
        assert len(db.load_expenses()) == 0
    
    def test_get_statistics(self, temp_db):
        """Test statistics calculation."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 10.00, "")
        db.append_expense("Food", 20.00, "")
        db.append_expense("Rent", 100.00, "")
        
        stats = db.get_statistics()
        assert stats['count'] == 3
        assert stats['total'] == 130.00
        assert abs(stats['average'] - 43.33) < 0.1
        assert stats['max'] == 100.00
        assert stats['min'] == 10.00


class TestImportExporter:
    """Tests for ImportExporter class."""
    
    def test_export_to_csv(self, temp_db, temp_dir):
        """Test exporting to CSV."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 15.00, "Lunch")
        db.append_expense("Rent", 500.00, "Monthly")
        
        csv_path = os.path.join(temp_dir, "export.csv")
        ImportExporter.export_to_csv(db, csv_path)
        
        assert os.path.exists(csv_path)
        
        # Verify CSV content
        with open(csv_path, 'r') as f:
            lines = f.readlines()
            assert len(lines) == 3  # Header + 2 expenses
            assert "Category" in lines[0]
    
    def test_export_to_json(self, temp_db, temp_dir):
        """Test exporting to JSON."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 15.00, "Lunch")
        db.append_expense("Rent", 500.00, "Monthly")
        
        json_path = os.path.join(temp_dir, "export.json")
        ImportExporter.export_to_json(db, json_path)
        
        assert os.path.exists(json_path)
        
        # Verify JSON content
        with open(json_path, 'r') as f:
            data = json.load(f)
            assert 'expenses' in data
            assert len(data['expenses']) == 2
            categories = {e['category'] for e in data['expenses']}
            assert categories == {'Food', 'Rent'}
    
    def test_import_from_csv(self, temp_db, temp_dir):
        """Test importing from CSV."""
        # Create a CSV file
        csv_path = os.path.join(temp_dir, "import.csv")
        with open(csv_path, 'w') as f:
            f.write("Category,Amount,Description\n")
            f.write("Food,15.00,Lunch\n")
            f.write("Rent,500.00,Monthly\n")
        
        db = ExpenseDatabase(temp_db)
        imported = ImportExporter.import_from_csv(db, csv_path)
        
        assert imported == 2
        assert db.get_total_spent() == 515.00
    
    def test_import_from_json(self, temp_db, temp_dir):
        """Test importing from JSON."""
        # Create a JSON file
        json_path = os.path.join(temp_dir, "import.json")
        data = {
            'expenses': [
                {'category': 'Food', 'amount': 15.00, 'description': 'Lunch'},
                {'category': 'Rent', 'amount': 500.00, 'description': 'Monthly'}
            ]
        }
        with open(json_path, 'w') as f:
            json.dump(data, f)
        
        db = ExpenseDatabase(temp_db)
        imported = ImportExporter.import_from_json(db, json_path)
        
        assert imported == 2
        assert db.get_total_spent() == 515.00
    
    def test_detect_format_csv(self):
        """Test CSV format detection."""
        assert ImportExporter.detect_format("file.csv") == "csv"
    
    def test_detect_format_json(self):
        """Test JSON format detection."""
        assert ImportExporter.detect_format("file.json") == "json"
    
    def test_detect_format_unknown(self):
        """Test unknown format detection."""
        assert ImportExporter.detect_format("file.txt") == "unknown"


class TestBackupManager:
    """Tests for BackupManager class."""
    
    def test_backup_creation(self, temp_db, temp_dir):
        """Test creating a backup."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 15.00, "Lunch")
        
        manager = BackupManager(temp_db, temp_dir)
        backup_path = manager.create_backup("Test backup")
        
        assert os.path.exists(backup_path)
        assert backup_path.endswith('.db')
    
    def test_list_backups(self, temp_db, temp_dir):
        """Test listing backups."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 15.00, "Lunch")
        
        manager = BackupManager(temp_db, temp_dir)
        backup1 = manager.create_backup("First backup")
        # Small delay to ensure different timestamps
        import time
        time.sleep(0.1)
        backup2 = manager.create_backup("Second backup")
        
        backups = manager.list_backups()
        assert len(backups) >= 2
    
    def test_restore_backup(self, temp_db, temp_dir):
        """Test restoring from backup."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 15.00, "Lunch")
        
        manager = BackupManager(temp_db, temp_dir)
        backup_path = manager.create_backup("Test backup")
        
        # Add more expenses to original
        db.append_expense("Rent", 500.00, "Monthly")
        assert db.get_total_spent() == 515.00
        
        # Restore backup
        manager.restore_backup(backup_path)
        
        # Check restored state by creating new connection
        db_restored = ExpenseDatabase(temp_db)
        total = db_restored.get_total_spent()
        assert total == 15.00
    
    def test_delete_backup(self, temp_db, temp_dir):
        """Test deleting a backup."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 15.00, "Lunch")
        
        manager = BackupManager(temp_db, temp_dir)
        backup_path = manager.create_backup("Test backup")
        assert os.path.exists(backup_path)
        
        deleted = manager.delete_backup(backup_path)
        assert deleted
        assert not os.path.exists(backup_path)
    
    def test_automatic_backup(self, temp_db, temp_dir):
        """Test automatic backup with cleanup."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 15.00, "Lunch")
        
        manager = BackupManager(temp_db, temp_dir)
        backup_path = manager.automatic_backup()
        
        assert os.path.exists(backup_path)
        
        backups = manager.list_backups()
        assert len(backups) > 0
    
    def test_get_backup_info(self, temp_db, temp_dir):
        """Test getting backup information."""
        db = ExpenseDatabase(temp_db)
        db.append_expense("Food", 15.00, "Lunch")
        db.append_expense("Rent", 500.00, "Monthly")
        
        manager = BackupManager(temp_db, temp_dir)
        backup_path = manager.create_backup()
        
        info = manager.get_backup_info(backup_path)
        assert 'size' in info
        assert 'created' in info
        assert info['record_count'] == 2


class TestDataMigration:
    """Tests for data migration scenarios."""
    
    def test_roundtrip_csv_export_import(self, temp_db, temp_dir):
        """Test exporting to CSV and importing back."""
        # Create original database
        db1 = ExpenseDatabase(temp_db)
        db1.append_expense("Food", 15.00, "Lunch")
        db1.append_expense("Rent", 500.00, "Monthly")
        original_total = db1.get_total_spent()
        
        # Export to CSV
        csv_path = os.path.join(temp_dir, "export.csv")
        ImportExporter.export_to_csv(db1, csv_path)
        
        # Create new database and import
        temp_db2 = os.path.join(temp_dir, "restored.db")
        db2 = ExpenseDatabase(temp_db2)
        imported = ImportExporter.import_from_csv(db2, csv_path)
        
        assert imported == 2
        assert db2.get_total_spent() == original_total
    
    def test_roundtrip_json_export_import(self, temp_db, temp_dir):
        """Test exporting to JSON and importing back."""
        # Create original database
        db1 = ExpenseDatabase(temp_db)
        db1.append_expense("Food", 15.00, "Lunch")
        db1.append_expense("Rent", 500.00, "Monthly")
        original_total = db1.get_total_spent()
        
        # Export to JSON
        json_path = os.path.join(temp_dir, "export.json")
        ImportExporter.export_to_json(db1, json_path)
        
        # Create new database and import
        temp_db2 = os.path.join(temp_dir, "restored.db")
        db2 = ExpenseDatabase(temp_db2)
        imported = ImportExporter.import_from_json(db2, json_path)
        
        assert imported == 2
        assert db2.get_total_spent() == original_total


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
