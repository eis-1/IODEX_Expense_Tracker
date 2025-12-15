import tkinter as tk
from tkinter import messagebox, ttk
import os
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
FILENAME = "expenses.txt"
def save_expense(category, amount, description):
    if not category or not amount:
        messagebox.showwarning("Missing Info", "Category and Amount are required.")
        return
    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Invalid Input", "Amount must be a number.") 
        return
    with open(FILENAME, "a") as file:
        file.write(f"{category},{amount},{description}\n")
    messagebox.showinfo("Saved", "Expense saved successfully!")
    main_menu()
def category_input(category):
    clear_window()
    tk.Label(root, text=f"Enter {category} Expense", font=("Comic Sans MS", 16, "bold"), bg="#AED6F1").pack(pady=10)
    tk.Label(root, text="Amount:", bg="#AED6F1").pack()
    amount_entry = tk.Entry(root)
    amount_entry.pack()
    tk.Label(root, text="Description:", bg="#AED6F1").pack()
    description_entry = tk.Entry(root)
    description_entry.pack()
    tk.Button(root, text="✅ OK", bg="#58D68D", fg="white",
              command=lambda: save_expense(category, amount_entry.get(), description_entry.get())).pack(pady=5)
    tk.Button(root, text="❌ Cancel", bg="#EC7063", fg="white", command=main_menu).pack()
    tk.Label(root, text="© 2025 IODEX. All rights reserved.", bg="#AED6F1", font=("Arial", 9, "italic")).pack(side="bottom", pady=5)
def add_expense_menu():
    clear_window()
    tk.Label(root, text="Choose a Category", font=("Comic Sans MS", 16, "bold"), bg="#AED6F1").pack(pady=10)
    for cat in ["Food", "Rent", "Utilities", "Shopping"]:
        tk.Button(root, text=cat, width=20, bg="#85C1E9", command=lambda c=cat: category_input(c)).pack(pady=2)
    tk.Label(root, text="© 2025 IODEX. All rights reserved.", bg="#AED6F1", font=("Arial", 9, "italic")).pack(side="bottom", pady=5)
def view_expenses():
    clear_window()
    if not os.path.exists(FILENAME):
        messagebox.showinfo("No Data", "No expenses recorded yet.")
        main_menu()
        return
    tk.Label(root, text="--- All Expenses ---", font=("Comic Sans MS", 16, "bold"), bg="#AED6F1").pack(pady=10)
    columns = ("Category", "Amount", "Description")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.pack(expand=True, fill="both", padx=20)
    total = 0
    with open(FILENAME, "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) == 3:
                tree.insert("", tk.END, values=parts)
                try:
                    total += float(parts[1])
                except:
                    pass
    tk.Label(root, text=f"💰 Total Spent: ${total:.2f}", font=("Arial", 12, "bold"), bg="#AED6F1").pack(pady=10)
    tk.Button(root, text="🔙 Back", bg="#D5DBDB", command=main_menu).pack(pady=10)
    tk.Label(root, text="© 2025 IODEX. All rights reserved.", bg="#AED6F1", font=("Arial", 9, "italic")).pack(side="bottom", pady=5)
def analyze_expenses():
    clear_window()
    if not os.path.exists(FILENAME):
        messagebox.showinfo("No Data", "No expenses to analyze.")
        main_menu()
        return
    try:
        df = pd.read_csv(FILENAME, names=["Category", "Amount", "Description"], on_bad_lines='skip')
        df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce')
        category_totals = df.groupby("Category")["Amount"].sum().sort_values()
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.barplot(x=category_totals.values, y=category_totals.index, palette="coolwarm", ax=ax)
        ax.set_title("Total Expenses by Category")
        ax.set_xlabel("Amount")
        ax.set_ylabel("Category")
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
        tk.Button(root, text="🔙 Back", bg="#D5DBDB", command=main_menu).pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", str(e))
def reset_expenses():
    if messagebox.askyesno("Reset", "Are you sure you want to delete all expenses?"):
        open(FILENAME, "w").close()
        messagebox.showinfo("Reset", "All expenses have been deleted.")
def clear_window():
    for widget in root.winfo_children():
        if widget != background_label:
            widget.destroy()
def main_menu():
    clear_window()
    tk.Label(root, text="🧾 Expense Tracker Menu", font=("Comic Sans MS", 16, "bold"), bg="#76D7C4").pack(pady=50)
    tk.Button(root, text="➕ Add Expense", width=30, bg="#A3E4D7", command=add_expense_menu).pack(pady=5)
    tk.Button(root, text="📄 View All Expenses", width=30, bg="#F9E79F", command=view_expenses).pack(pady=5)
    tk.Button(root, text="📊 Analyze Expenses", width=30, bg="#D2B4DE", command=analyze_expenses).pack(pady=5)
    tk.Button(root, text="🗑 Reset Expenses", width=30, bg="#F5B7B1", command=reset_expenses).pack(pady=5)
    tk.Button(root, text="💾 Save Expenses", width=30, bg="#AED6F1",
              command=lambda: messagebox.showinfo("Saved", "All expenses already saved automatically.")).pack(pady=5)
    tk.Button(root, text="❌ Exit", width=30, bg="#D7DBDD", command=root.quit).pack(pady=5)
    tk.Label(root, text="© 2025 IODEX. All rights reserved.", bg="#B3E5FC", font=("Arial", 9, "italic")).pack(side="bottom", pady=5)
root = tk.Tk()
root.title("IODEX Expense Tracker")
root.geometry("700x500")
try:
    image = Image.open("photo1.jpg").resize((700, 500), Image.Resampling.LANCZOS)
    photo1 = ImageTk.PhotoImage(image)
    background_label = tk.Label(root, image=photo1)
    background_label.image = photo1  # Keep a reference
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print("Background image error:", e)
    background_label = tk.Label(root, bg="#FFFF8F")
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
main_menu()
root.mainloop()