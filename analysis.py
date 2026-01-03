"""
Analysis module for expense data visualization and aggregation.
Generates charts and summary statistics for expense data.
Supports both CSV (legacy) and SQLite (current) storage backends.
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import os
from storage import load_expenses, DEFAULT_FILENAME
from database import ExpenseDatabase


def get_category_totals(path: str = DEFAULT_FILENAME) -> dict:
    """
    Calculate total expenses grouped by category (CSV mode).
    
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
    for category, amount, *_ in expenses:
        if category in category_totals:
            category_totals[category] += amount
        else:
            category_totals[category] = amount
    
    return category_totals


def get_category_totals_db(db: ExpenseDatabase) -> dict:
    """
    Calculate total expenses grouped by category (Database mode).
    
    Args:
        db: ExpenseDatabase instance
    
    Returns:
        Dictionary with category names as keys and total amounts as values.
    """
    return db.get_category_totals()


def create_category_chart(path: str = DEFAULT_FILENAME, top_n: int | None = None):
    """
    Create an improved bar chart of total expenses by category (CSV mode).

    Args:
        path: File path to read from (defaults to expenses.txt)
        top_n: If provided, show only the top N categories

    Returns:
        matplotlib figure object ready for embedding in GUI

    Raises:
        ValueError: If no expense data exists
    """
    try:
        df = pd.read_csv(path, names=["Category", "Amount", "Description", "Timestamp"], 
                        on_bad_lines='skip', quoting=csv.QUOTE_ALL)

        if df.empty:
            raise ValueError("No expense data available for analysis.")

        df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
        category_totals = df.groupby("Category")["Amount"].sum().sort_values(ascending=False)

        if top_n is not None:
            category_totals = category_totals.head(top_n)

        # Modern style and palette
        sns.set_theme(style='whitegrid')
        fig, ax = plt.subplots(figsize=(8, max(4, 0.5 * len(category_totals))))
        colors = sns.color_palette("viridis", len(category_totals))
        bars = ax.barh(category_totals.index[::-1], category_totals.values[::-1], color=colors)

        ax.set_title("Total Expenses by Category")
        ax.set_xlabel("Amount ($)")
        ax.set_ylabel("")

        # Annotate bars with amounts and percentages
        total = category_totals.sum()
        for bar, value in zip(bars, category_totals.values[::-1]):
            w = bar.get_width()
            pct = (value / total * 100) if total != 0 else 0
            ax.text(w + total * 0.005, bar.get_y() + bar.get_height() / 2, f"${w:.2f} ({pct:.0f}%)", va='center')

        fig.tight_layout()
        return fig

    except Exception as e:
        raise ValueError(f"Failed to create chart: {str(e)}")


# Plotly integration for interactive charts
def create_category_chart_plotly(path: str = DEFAULT_FILENAME, top_n: int | None = None):
    """
    Create an interactive Plotly bar chart (returns a Plotly Figure)
    """
    try:
        import plotly.express as px
        df = pd.read_csv(path, names=["Category", "Amount", "Description", "Timestamp"], on_bad_lines='skip', quoting=csv.QUOTE_ALL)
        if df.empty:
            raise ValueError("No expense data available for analysis.")
        df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
        category_totals = df.groupby("Category")["Amount"].sum().reset_index().sort_values(by="Amount", ascending=False)
        if top_n is not None:
            category_totals = category_totals.head(top_n)
        total = category_totals["Amount"].sum()
        category_totals["pct"] = (category_totals["Amount"] / total * 100).round(1)
        fig = px.bar(category_totals, x="Amount", y="Category", orientation='h', color="Amount", color_continuous_scale='Viridis', hover_data={"Amount":":.2f", "pct":"auto"})
        fig.update_layout(title_text="Total Expenses by Category (interactive)", yaxis={'categoryorder':'total ascending'})
        return fig
    except Exception as e:
        raise ValueError(f"Failed to create interactive chart: {str(e)}")


def open_interactive_chart(path: str = DEFAULT_FILENAME, top_n: int | None = None, auto_open: bool = True) -> str:
    """Open the interactive Plotly chart.

    If `pywebview` is available, open in an embedded webview window. Otherwise,
    write a temporary HTML file and open in the default browser (or return the
    path when `auto_open` is False).
    Returns the path to the generated HTML file.
    """
    fig = create_category_chart_plotly(path, top_n=top_n)
    import plotly.offline as pyo
    import tempfile
    tmp = tempfile.NamedTemporaryFile(suffix='.html', delete=False)
    pyo.plot(fig, filename=tmp.name, auto_open=False)
    html_path = tmp.name

    if auto_open:
        # Prefer an embedded window using pywebview if available
        try:
            import webview
            # Create a webview window in a non-blocking fashion
            def _open():
                webview.create_window('Interactive Chart', html_path)
                webview.start()
            import threading
            t = threading.Thread(target=_open, daemon=True)
            t.start()
        except Exception:
            # Fallback to opening in the default browser
            import webbrowser
            webbrowser.open(f'file://{html_path}')

    return html_path


def create_category_chart_db(db: ExpenseDatabase):
    """
    Create a bar chart of total expenses by category (Database mode).
    
    Args:
        db: ExpenseDatabase instance
    
    Returns:
        matplotlib figure object ready for embedding in GUI
        
    Raises:
        ValueError: If no expense data exists
    """
    try:
        category_totals_dict = db.get_category_totals()
        
        if not category_totals_dict:
            raise ValueError("No expense data available for analysis.")
        
        # Convert to Series for plotting
        category_totals = pd.Series(category_totals_dict).sort_values()
        
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
    Generate summary statistics for expense data (CSV mode).
    
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
    
    amounts = [exp[1] for exp in expenses]
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


def get_summary_stats_db(db: ExpenseDatabase) -> dict:
    """
    Generate summary statistics for expense data (Database mode).
    
    Args:
        db: ExpenseDatabase instance
    
    Returns:
        Dictionary with comprehensive statistics
    """
    return db.get_statistics()
