import os
import sqlite3
import csv

CSV_FILE = "expenses.txt"
DB_FILE = "expenses.db"

def read_csv_expenses(csv_path):
    expenses = []
    if not os.path.exists(csv_path):
        print(f"CSV file '{csv_path}' not found.")
        return expenses
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 4:
                category, amount, description, timestamp = row[:4]
                expenses.append((category, float(amount), description, timestamp))
    return expenses

def ensure_db_schema(db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            amount REAL NOT NULL CHECK(amount >= 0),
            description TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def insert_expenses_to_db(db_path, expenses):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    for category, amount, description, timestamp in expenses:
        c.execute(
            "INSERT INTO expenses (category, amount, description, timestamp) VALUES (?, ?, ?, ?)",
            (category, amount, description, timestamp)
        )
    conn.commit()
    conn.close()

def main():
    expenses = read_csv_expenses(CSV_FILE)
    if not expenses:
        print("No expenses found to migrate.")
        return
    ensure_db_schema(DB_FILE)
    insert_expenses_to_db(DB_FILE, expenses)
    print("Migration Successful")

if __name__ == "__main__":
    main()