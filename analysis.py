"""
Analysis module for expense data visualization and aggregation.
Generates charts and summary statistics for expense data.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
from storage import load_expenses, DEFAULT_FILENAME


def get_category_totals(path: str = DEFAULT_FILENAME) -> dict:
    """
    Calculate total expenses grouped by category.
    
    Args:
        path: File path to read from (defaults to expenses.txt)
    
    Returns:
        Dictionary with category names as keys and total amounts as values.
        Returns empty dict if no expenses exist.
    """
    expenses = load_expenses(path)
    
    if not expenses:
        return {}
    
    category_totals = {}
    for category, amount, _ in expenses:
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    
    return category_totals


def create_category_chart(path: str = DEFAULT_FILENAME):
    """
    Create a bar chart of total expenses by category.
    
    Args:
        path: File path to read from (defaults to expenses.txt)
    
    Returns:
        matplotlib figure object ready for embedding in GUI
        
    Raises:
        ValueError: If no expense data exists
    """
    try:
        df = pd.read_csv(path, names=["Category", "Amount", "Description"], 
                        on_bad_lines='skip', quoting=csv.QUOTE_ALL)
        
        if df.empty:
            raise ValueError("No expense data available for analysis.")
        
        df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
        category_totals = df.groupby("Category")["Amount"].sum().sort_values()
        
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=category_totals.values, y=category_totals.index, 
                   palette="coolwarm", ax=ax)
        ax.set_title("Total Expenses by Category")
        ax.set_xlabel("Amount ($)")
        ax.set_ylabel("Category")
        fig.tight_layout()
        
        return fig
    
    except Exception as e:
        raise ValueError(f"Failed to create chart: {str(e)}")


def get_summary_stats(path: str = DEFAULT_FILENAME) -> dict:
    """
    Generate summary statistics for expense data.
    
    Args:
        path: File path to read from (defaults to expenses.txt)
    
    Returns:
        Dictionary with keys: 'total', 'average', 'count', 'max_category'
        Returns None values if no expenses exist.
    """
    expenses = load_expenses(path)
    
    if not expenses:
        return {
            'total': 0.0,
            'average': 0.0,
            'count': 0,
            'max_category': None
        }
    
    amounts = [amount for _, amount, _ in expenses]
    category_totals = get_category_totals(path)
    
    total = sum(amounts)
    average = total / len(amounts) if amounts else 0.0
    max_category = max(category_totals, key=category_totals.get) if category_totals else None
    
    return {
        'total': total,
        'average': average,
        'count': len(expenses),
        'max_category': max_category
    }
