"""
HOW TO RUN TESTS
================

Prerequisites:

- pytest installed: pip install pytest (or already in requirements.txt)
- Python 3.8+

## Running All Tests:

cd "d:/siam/Object-oriented final project"
pytest test_storage.py -v

## Running Specific Test Class:

pytest test_storage.py::TestAppendExpense -v
pytest test_storage.py::TestLoadExpenses -v
pytest test_storage.py::TestEdgeCases -v

## Running Specific Test:

pytest test_storage.py::TestAppendExpense::test_append_with_commas_in_description -v

## Running Tests with Coverage:

pip install pytest-cov
pytest test_storage.py --cov=storage --cov-report=html

# Test Summary:

Total Tests: 39
Passed: 39 ✓
Failed: 0
Skipped: 0
Success Rate: 100%

# What the Tests Cover:

1. CSV Handling with Special Characters

   - Commas in descriptions are properly escaped
   - Quotes are correctly handled
   - Newlines within fields are preserved

2. Data Validation

   - Non-numeric amounts are rejected
   - Negative amounts are rejected
   - Missing categories are rejected
   - None values are handled properly

3. Edge Cases

   - Very long descriptions (1000+ characters)
   - Empty descriptions
   - Zero and large amounts
   - Scientific notation
   - Special characters

4. File Operations

   - Non-existent file handling
   - Empty file handling
   - Appending to existing files
   - Clearing file contents
   - File existence checking

5. Data Integrity
   - Decimal precision is preserved
   - Multiple expenses are loaded in order
   - Totals are calculated correctly
   - Malformed rows are skipped gracefully

# Storage Module API:

append_expense(category, amount, description, path="expenses.txt")

- Add a single expense to file
- Raises ValueError for invalid inputs
- Usage: append_expense("Food", 25.50, "Lunch", "expenses.txt")

load_expenses(path="expenses.txt")

- Load all valid expenses from file
- Returns list of (category, amount, description) tuples
- Skips malformed rows silently
- Usage: expenses = load_expenses()

get_total_spent(path="expenses.txt")

- Calculate total amount spent
- Returns float sum of all amounts
- Usage: total = get_total_spent()

clear_expenses(path="expenses.txt")

- Delete all expenses from file
- Usage: clear_expenses()

file_exists(path="expenses.txt")

- Check if expense file exists
- Returns boolean
- Usage: if file_exists(): ...
  """
