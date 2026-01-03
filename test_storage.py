"""
Unit tests for the storage module.
Tests parsing edge cases, data validation, and CSV handling.

Run with: pytest test_storage.py -v
"""
import pytest
import os
import tempfile
import csv
from storage import (
    append_expense,
    load_expenses,
    get_total_spent,
    clear_expenses,
    file_exists
)


@pytest.fixture
def temp_file():
    """Create a temporary file for testing."""
    fd, path = tempfile.mkstemp(suffix='.txt')
    os.close(fd)
    yield path
    # Cleanup
    if os.path.exists(path):
        os.remove(path)


class TestAppendExpense:
    """Tests for the append_expense function."""
    
    def test_append_valid_expense(self, temp_file):
        """Test appending a valid expense."""
        append_expense("Food", 10.50, "Lunch", temp_file)
        expenses = load_expenses(temp_file)
        assert len(expenses) == 1
        assert expenses[0] == ("Food", 10.50, "Lunch")
    
    def test_append_multiple_expenses(self, temp_file):
        """Test appending multiple expenses."""
        append_expense("Food", 10.50, "Lunch", temp_file)
        append_expense("Rent", 500.00, "Monthly rent", temp_file)
        expenses = load_expenses(temp_file)
        assert len(expenses) == 2
    
    def test_append_with_commas_in_description(self, temp_file):
        """Test that commas in descriptions are properly escaped."""
        append_expense("Food", 15.00, "Coffee, sandwich, and pastry", temp_file)
        expenses = load_expenses(temp_file)
        assert len(expenses) == 1
        assert expenses[0][2] == "Coffee, sandwich, and pastry"
    
    def test_append_with_quotes_in_description(self, temp_file):
        """Test that quotes in descriptions are properly escaped."""
        append_expense("Shopping", 25.00, 'Book: "The Python Way"', temp_file)
        expenses = load_expenses(temp_file)
        assert len(expenses) == 1
        assert expenses[0][2] == 'Book: "The Python Way"'
    
    def test_append_with_newlines_in_description(self, temp_file):
        """Test handling of newlines in descriptions."""
        append_expense("Notes", 0.00, "Line 1\nLine 2", temp_file)
        expenses = load_expenses(temp_file)
        assert len(expenses) == 1
        assert expenses[0][2] == "Line 1\nLine 2"
    
    def test_append_empty_description(self, temp_file):
        """Test appending with empty description."""
        append_expense("Utilities", 50.00, "", temp_file)
        expenses = load_expenses(temp_file)
        assert len(expenses) == 1
        assert expenses[0] == ("Utilities", 50.00, "")
    
    def test_append_zero_amount(self, temp_file):
        """Test appending with zero amount."""
        append_expense("Test", 0.0, "Free item", temp_file)
        expenses = load_expenses(temp_file)
        assert len(expenses) == 1
        assert expenses[0][1] == 0.0
    
    def test_append_large_amount(self, temp_file):
        """Test appending with large amount."""
        append_expense("Investment", 1000000.99, "Big purchase", temp_file)
        expenses = load_expenses(temp_file)
        assert expenses[0][1] == 1000000.99
    
    def test_append_float_string_amount(self, temp_file):
        """Test that string amounts are converted to float."""
        append_expense("Food", "12.50", "Dinner", temp_file)
        expenses = load_expenses(temp_file)
        assert expenses[0][1] == 12.50
        assert isinstance(expenses[0][1], float)
    
    def test_append_invalid_amount_non_numeric(self, temp_file):
        """Test that non-numeric amounts raise ValueError."""
        with pytest.raises(ValueError, match="Amount must be a number"):
            append_expense("Food", "abc", "Lunch", temp_file)
    
    def test_append_invalid_amount_none(self, temp_file):
        """Test that None amount raises ValueError."""
        with pytest.raises(ValueError, match="Amount must be a number"):
            append_expense("Food", None, "Lunch", temp_file)
    
    def test_append_missing_category(self, temp_file):
        """Test that missing category raises ValueError."""
        with pytest.raises(ValueError, match="Category and Amount are required"):
            append_expense("", 10.0, "Description", temp_file)
    
    def test_append_negative_amount(self, temp_file):
        """Test that negative amounts raise ValueError."""
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            append_expense("Food", -10.0, "Refund", temp_file)
    
    def test_append_special_characters_in_category(self, temp_file):
        """Test category with special characters."""
        append_expense("Food & Drinks", 20.00, "Brunch", temp_file)
        expenses = load_expenses(temp_file)
        assert expenses[0][0] == "Food & Drinks"


class TestLoadExpenses:
    """Tests for the load_expenses function."""
    
    def test_load_nonexistent_file(self, temp_file):
        """Test loading from nonexistent file returns empty list."""
        os.remove(temp_file)
        expenses = load_expenses(temp_file)
        assert expenses == []
    
    def test_load_empty_file(self, temp_file):
        """Test loading from empty file returns empty list."""
        expenses = load_expenses(temp_file)
        assert expenses == []
    
    def test_load_single_expense(self, temp_file):
        """Test loading single expense."""
        append_expense("Food", 15.00, "Lunch", temp_file)
        expenses = load_expenses(temp_file)
        assert len(expenses) == 1
        assert expenses[0] == ("Food", 15.00, "Lunch")
    
    def test_load_multiple_expenses(self, temp_file):
        """Test loading multiple expenses maintains order."""
        append_expense("Food", 10.00, "Breakfast", temp_file)
        append_expense("Rent", 500.00, "Monthly", temp_file)
        append_expense("Utilities", 50.00, "Electric", temp_file)
        
        expenses = load_expenses(temp_file)
        assert len(expenses) == 3
        assert expenses[0][0] == "Food"
        assert expenses[1][0] == "Rent"
        assert expenses[2][0] == "Utilities"
    
    def test_load_skips_malformed_rows_invalid_amount(self, temp_file):
        """Test that rows with invalid amounts are skipped."""
        with open(temp_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Food", 10.00, "Valid"])
            writer.writerow(["Rent", "invalid", "Skip this"])
            writer.writerow(["Utilities", 50.00, "Also valid"])
        
        expenses = load_expenses(temp_file)
        assert len(expenses) == 2
        assert expenses[0][0] == "Food"
        assert expenses[1][0] == "Utilities"
    
    def test_load_skips_negative_amounts(self, temp_file):
        """Test that rows with negative amounts are skipped."""
        with open(temp_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Food", 10.00, "Valid"])
            writer.writerow(["Refund", -50.00, "Skip negative"])
        
        expenses = load_expenses(temp_file)
        assert len(expenses) == 1
        assert expenses[0][0] == "Food"
    
    def test_load_skips_incomplete_rows(self, temp_file):
        """Test that rows with < 3 fields are skipped."""
        with open(temp_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Food", 10.00, "Valid"])
            writer.writerow(["Incomplete"])
            writer.writerow(["Still", "incomplete"])
        
        expenses = load_expenses(temp_file)
        assert len(expenses) == 1
        assert expenses[0][0] == "Food"
    
    def test_load_handles_quoted_fields(self, temp_file):
        """Test that quoted CSV fields are properly parsed."""
        with open(temp_file, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Food", 15.00, "Complex, description with, commas"])
        
        expenses = load_expenses(temp_file)
        assert len(expenses) == 1
        assert "commas" in expenses[0][2]
    
    def test_load_preserves_decimal_precision(self, temp_file):
        """Test that decimal amounts are preserved."""
        append_expense("Food", 10.99, "Item", temp_file)
        expenses = load_expenses(temp_file)
        assert expenses[0][1] == 10.99


class TestGetTotalSpent:
    """Tests for the get_total_spent function."""
    
    def test_total_empty_file(self, temp_file):
        """Test total from empty file is 0.0."""
        total = get_total_spent(temp_file)
        assert total == 0.0
    
    def test_total_single_expense(self, temp_file):
        """Test total with single expense."""
        append_expense("Food", 10.50, "Lunch", temp_file)
        total = get_total_spent(temp_file)
        assert total == 10.50
    
    def test_total_multiple_expenses(self, temp_file):
        """Test total with multiple expenses."""
        append_expense("Food", 10.00, "", temp_file)
        append_expense("Rent", 500.00, "", temp_file)
        append_expense("Utilities", 50.00, "", temp_file)
        total = get_total_spent(temp_file)
        assert total == 560.00
    
    def test_total_with_floats(self, temp_file):
        """Test total calculation with floating point numbers."""
        append_expense("Food", 10.99, "", temp_file)
        append_expense("Food", 15.01, "", temp_file)
        total = get_total_spent(temp_file)
        assert abs(total - 26.00) < 0.01  # Account for floating point errors
    
    def test_total_skips_malformed_rows(self, temp_file):
        """Test that malformed rows don't affect total."""
        append_expense("Food", 10.00, "", temp_file)
        with open(temp_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Invalid", "abc", ""])
        append_expense("Rent", 50.00, "", temp_file)
        
        total = get_total_spent(temp_file)
        assert total == 60.00


class TestClearExpenses:
    """Tests for the clear_expenses function."""
    
    def test_clear_existing_file(self, temp_file):
        """Test clearing a file with expenses."""
        append_expense("Food", 10.00, "Item", temp_file)
        assert get_total_spent(temp_file) == 10.00
        
        clear_expenses(temp_file)
        
        expenses = load_expenses(temp_file)
        assert expenses == []
        assert get_total_spent(temp_file) == 0.0
    
    def test_clear_empty_file(self, temp_file):
        """Test clearing an empty file."""
        clear_expenses(temp_file)
        expenses = load_expenses(temp_file)
        assert expenses == []
    
    def test_clear_then_append(self, temp_file):
        """Test appending after clearing."""
        append_expense("Food", 10.00, "Item", temp_file)
        clear_expenses(temp_file)
        append_expense("New", 5.00, "New item", temp_file)
        
        expenses = load_expenses(temp_file)
        assert len(expenses) == 1
        assert expenses[0][0] == "New"


class TestFileExists:
    """Tests for the file_exists function."""
    
    def test_file_exists_when_created(self, temp_file):
        """Test that file_exists returns True for existing file."""
        assert file_exists(temp_file)
    
    def test_file_not_exists_when_removed(self, temp_file):
        """Test that file_exists returns False after deletion."""
        os.remove(temp_file)
        assert not file_exists(temp_file)
    
    def test_file_exists_after_append(self, temp_file):
        """Test that file_exists returns True after appending."""
        os.remove(temp_file)
        assert not file_exists(temp_file)
        
        append_expense("Food", 10.00, "Item", temp_file)
        assert file_exists(temp_file)


class TestEdgeCases:
    """Tests for edge cases and special scenarios."""
    
    def test_special_characters_in_description(self, temp_file):
        """Test handling of special characters in descriptions."""
        append_expense("Food", 10.00, "Item with @#$% symbols", temp_file)
        expenses = load_expenses(temp_file)
        assert "@#$%" in expenses[0][2]
    
    def test_very_long_description(self, temp_file):
        """Test handling of very long descriptions."""
        long_desc = "x" * 1000
        append_expense("Item", 5.00, long_desc, temp_file)
        expenses = load_expenses(temp_file)
        assert expenses[0][2] == long_desc
    
    def test_whitespace_in_category(self, temp_file):
        """Test category with whitespace."""
        append_expense("  Food Items  ", 10.00, "Description", temp_file)
        expenses = load_expenses(temp_file)
        assert expenses[0][0] == "  Food Items  "
    
    def test_amount_scientific_notation(self, temp_file):
        """Test scientific notation amounts."""
        append_expense("Test", 1.5e2, "Scientific notation", temp_file)
        expenses = load_expenses(temp_file)
        assert expenses[0][1] == 150.0
    
    def test_many_expenses(self, temp_file):
        """Test handling many expenses."""
        for i in range(100):
            append_expense(f"Cat{i % 5}", float(i), f"Expense {i}", temp_file)
        
        expenses = load_expenses(temp_file)
        assert len(expenses) == 100
        
        total = get_total_spent(temp_file)
        expected = sum(range(100))
        assert abs(total - expected) < 0.01


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
