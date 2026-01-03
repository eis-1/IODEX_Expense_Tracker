"""
GUI module for IODEX Expense Tracker.
Handles all user interface rendering and interaction logic.
"""
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import storage
from storage import DEFAULT_FILENAME
import analysis


class ExpenseTrackerGUI:
    """Main GUI application class for the expense tracker."""
    
    def __init__(self, root, filepath: str = DEFAULT_FILENAME):
        """
        Initialize the GUI application.
        
        Args:
            root: Tkinter root window
            filepath: Path to expense storage file (defaults to expenses.txt)
        """
        self.root = root
        self.filepath = filepath
        self.root.title("IODEX Expense Tracker")
        self.root.geometry("700x500")
        
        # Setup background
        self.background_label = self._setup_background()
        
        # Category options
        self.categories = ["Food", "Rent", "Utilities", "Shopping"]
        
        # Display main menu
        self.main_menu()
    
    def _setup_background(self):
        """
        Setup background image or solid color fallback.
        
        Returns:
            Label widget containing the background
        """
        try:
            image = Image.open("photo1.jpg").resize((700, 500), Image.Resampling.LANCZOS)
            photo1 = ImageTk.PhotoImage(image)
            background_label = tk.Label(self.root, image=photo1)
            background_label.image = photo1  # Keep a reference
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            return background_label
        except Exception as e:
            print("Background image error:", e)
            background_label = tk.Label(self.root, bg="#FFFF8F")
            background_label.place(x=0, y=0, relwidth=1, relheight=1)
            return background_label
    
    def _clear_window(self):
        """Remove all widgets except the background label."""
        for widget in self.root.winfo_children():
            if widget != self.background_label:
                widget.destroy()
    
    def _add_footer(self):
        """Add copyright footer to the current window."""
        tk.Label(self.root, text="© 2025 IODEX. All rights reserved.", 
                bg="#B3E5FC", font=("Arial", 9, "italic")).pack(side="bottom", pady=5)
    
    def main_menu(self):
        """Display the main menu screen."""
        self._clear_window()
        
        tk.Label(self.root, text="🧾 Expense Tracker Menu", 
                font=("Comic Sans MS", 16, "bold"), bg="#76D7C4").pack(pady=50)
        
        tk.Button(self.root, text="➕ Add Expense", width=30, bg="#A3E4D7", 
                 command=self.add_expense_menu).pack(pady=5)
        tk.Button(self.root, text="📄 View All Expenses", width=30, bg="#F9E79F", 
                 command=self.view_expenses).pack(pady=5)
        tk.Button(self.root, text="📊 Analyze Expenses", width=30, bg="#D2B4DE", 
                 command=self.analyze_expenses).pack(pady=5)
        tk.Button(self.root, text="🗑 Reset Expenses", width=30, bg="#F5B7B1", 
                 command=self.reset_expenses).pack(pady=5)
        tk.Button(self.root, text="💾 Save Expenses", width=30, bg="#AED6F1",
                 command=lambda: messagebox.showinfo("Saved", 
                 "All expenses already saved automatically.")).pack(pady=5)
        tk.Button(self.root, text="❌ Exit", width=30, bg="#D7DBDD", 
                 command=self.root.quit).pack(pady=5)
        
        self._add_footer()
    
    def add_expense_menu(self):
        """Display the category selection menu for adding expenses."""
        self._clear_window()
        
        tk.Label(self.root, text="Choose a Category", 
                font=("Comic Sans MS", 16, "bold"), bg="#AED6F1").pack(pady=10)
        
        for cat in self.categories:
            tk.Button(self.root, text=cat, width=20, bg="#85C1E9", 
                     command=lambda c=cat: self.category_input(c)).pack(pady=2)
        
        tk.Label(self.root, text="© 2025 IODEX. All rights reserved.", 
                bg="#AED6F1", font=("Arial", 9, "italic")).pack(side="bottom", pady=5)
    
    def category_input(self, category):
        """
        Display the input form for a specific expense category.
        
        Args:
            category: The selected expense category
        """
        self._clear_window()
        
        tk.Label(self.root, text=f"Enter {category} Expense", 
                font=("Comic Sans MS", 16, "bold"), bg="#AED6F1").pack(pady=10)
        
        tk.Label(self.root, text="Amount:", bg="#AED6F1").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack()
        
        tk.Label(self.root, text="Description:", bg="#AED6F1").pack()
        description_entry = tk.Entry(self.root)
        description_entry.pack()
        
        tk.Button(self.root, text="✅ OK", bg="#58D68D", fg="white",
                 command=lambda: self._save_expense_wrapper(
                     category, amount_entry.get(), description_entry.get())).pack(pady=5)
        tk.Button(self.root, text="❌ Cancel", bg="#EC7063", fg="white", 
                 command=self.main_menu).pack()
        
        tk.Label(self.root, text="© 2025 IODEX. All rights reserved.", 
                bg="#AED6F1", font=("Arial", 9, "italic")).pack(side="bottom", pady=5)
    
    def _save_expense_wrapper(self, category, amount, description):
        """
        Wrapper for saving expense with error handling.
        
        Args:
            category: Expense category
            amount: Expense amount
            description: Expense description
        """
        try:
            storage.append_expense(category, amount, description, self.filepath)
            messagebox.showinfo("Saved", "Expense saved successfully!")
            self.main_menu()
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
    
    def view_expenses(self):
        """Display all recorded expenses in a table view."""
        self._clear_window()
        
        if not storage.file_exists(self.filepath):
            messagebox.showinfo("No Data", "No expenses recorded yet.")
            self.main_menu()
            return
        
        tk.Label(self.root, text="--- All Expenses ---", 
                font=("Comic Sans MS", 16, "bold"), bg="#AED6F1").pack(pady=10)
        
        columns = ("Category", "Amount", "Description")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.pack(expand=True, fill="both", padx=20)
        
        # Load and display expenses
        expenses = storage.load_expenses(self.filepath)
        for category, amount, description in expenses:
            tree.insert("", tk.END, values=(category, f"${amount:.2f}", description))
        
        total = storage.get_total_spent(self.filepath)
        tk.Label(self.root, text=f"💰 Total Spent: ${total:.2f}", 
                font=("Arial", 12, "bold"), bg="#AED6F1").pack(pady=10)
        
        tk.Button(self.root, text="🔙 Back", bg="#D5DBDB", 
                 command=self.main_menu).pack(pady=10)
        
        tk.Label(self.root, text="© 2025 IODEX. All rights reserved.", 
                bg="#AED6F1", font=("Arial", 9, "italic")).pack(side="bottom", pady=5)
    
    def analyze_expenses(self):
        """Display analysis chart of expenses by category."""
        self._clear_window()
        
        if not storage.file_exists(self.filepath):
            messagebox.showinfo("No Data", "No expenses to analyze.")
            self.main_menu()
            return
        
        try:
            fig = analysis.create_category_chart(self.filepath)
            
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)
            
            tk.Button(self.root, text="🔙 Back", bg="#D5DBDB", 
                     command=self.main_menu).pack(pady=10)
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.main_menu()
    
    def reset_expenses(self):
        """Clear all expense records after user confirmation."""
        if messagebox.askyesno("Reset", "Are you sure you want to delete all expenses?"):
            storage.clear_expenses(self.filepath)
            messagebox.showinfo("Reset", "All expenses have been deleted.")
            self.main_menu()


def run_application(filepath: str = DEFAULT_FILENAME):
    """Launch the expense tracker application.
    
    Args:
        filepath: Path to expense storage file (defaults to expenses.txt)
    """
    root = tk.Tk()
    app = ExpenseTrackerGUI(root, filepath)
    root.mainloop()


if __name__ == "__main__":
    run_application()
