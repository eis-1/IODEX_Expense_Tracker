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
        import config
        self.root = root
        self.filepath = filepath
        self.config = config.load_config()

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
        tk.Button(self.root, text="⚙ Preferences", width=30, bg="#FAD7A0",
                 command=self.open_preferences).pack(pady=5)
        tk.Button(self.root, text="💾 Save Expenses", width=30, bg="#AED6F1",
                 command=lambda: messagebox.showinfo("Saved", 
                 "All expenses already saved automatically.")).pack(pady=5)
        tk.Button(self.root, text="❌ Exit", width=30, bg="#D7DBDD", 
                 command=self._on_exit).pack(pady=5)
        
        self._add_footer()
    
    def add_expense_menu(self):
        """Display the category selection menu for adding expenses."""
        self._clear_window()
        
        tk.Label(self.root, text="Choose a Category", 
                font=("Comic Sans MS", 16, "bold"), bg="#AED6F1").pack(pady=10)
        
        for cat in self.categories:
            tk.Button(self.root, text=cat, width=20, bg="#85C1E9", 
                     command=lambda c=cat: self.category_input(c)).pack(pady=2)

        # Back button to return to main menu (ensure visible on small displays)
        tk.Button(self.root, text="🔙 Back", bg="#D5DBDB", command=self.main_menu).pack(pady=8)

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
        # Explicit Back button for clarity and accessibility
        tk.Button(self.root, text="🔙 Back", bg="#D5DBDB", command=self.main_menu).pack(pady=6)
        
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
        
        columns = ("Category", "Amount", "Description", "Timestamp")
        tree = ttk.Treeview(self.root, columns=columns, show="headings")
        
        for col in columns:
            tree.heading(col, text=col)
        
        tree.pack(expand=True, fill="both", padx=20)
        
        # Load and display expenses
        import utils
        expenses = storage.load_expenses(self.filepath)
        for category, amount, description, *rest in expenses:
            timestamp = rest[0] if rest else ""
            # Format timestamp according to user's preference
            mode = self.config.get('timestamp_mode', 'local')
            custom_fmt = self.config.get('custom_format', '%Y-%m-%d %H:%M:%S %Z')
            show_rel = bool(self.config.get('show_relative', True))
            ts_display = utils.format_iso_timestamp(timestamp, mode=mode, custom_fmt=custom_fmt, show_relative=show_rel) if timestamp else ""
            tree.insert("", tk.END, values=(category, f"${amount:.2f}", description, ts_display))
        
        total = storage.get_total_spent(self.filepath)
        tk.Label(self.root, text=f"💰 Total Spent: ${total:.2f}", 
                font=("Arial", 12, "bold"), bg="#AED6F1").pack(pady=10)
        
        tk.Button(self.root, text="Delete Selected", bg="#F5B7B1", command=lambda: self._delete_selected(tree)).pack(pady=2)
        tk.Button(self.root, text="🔙 Back", bg="#D5DBDB", 
                 command=self.main_menu).pack(pady=10)
        
        tk.Label(self.root, text="© 2025 IODEX. All rights reserved.", 
                bg="#AED6F1", font=("Arial", 9, "italic")).pack(side="bottom", pady=5)

    def _delete_selected(self, tree: ttk.Treeview):
        """Delete the selected rows from storage after confirmation.

        This method handles CSV-based storage deletion by identifying the expense
        from the tree values (category, $amount, description, timestamp).
        """
        selected = tree.selection()
        if not selected:
            messagebox.showinfo("Delete", "Please select one or more expenses to delete.")
            return

        if not messagebox.askyesno("Delete", "Are you sure you want to delete the selected expense(s)?"):
            return

        deleted_any = False
        for item in selected:
            vals = tree.item(item)['values']
            # Expect values: (category, '$amount', description, timestamp)
            category = vals[0]
            amount_str = str(vals[1]).lstrip('$').replace(',', '')
            try:
                amount = float(amount_str)
            except Exception:
                continue
            description = vals[2]
            timestamp = vals[3] if len(vals) >= 4 else None
            if storage.delete_expense(category, amount, description, timestamp, path=self.filepath):
                deleted_any = True

        if deleted_any:
            messagebox.showinfo("Delete", "Selected expenses have been deleted.")
            self.view_expenses()
        else:
            messagebox.showinfo("Delete", "No matching expenses were found to delete.")    
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

            tk.Button(self.root, text="⬇ Export Image", bg="#AED6F1", command=lambda: self._export_chart(fig)).pack(pady=2)
            tk.Button(self.root, text="🌐 Open Interactive Chart", bg="#AED6F1", command=lambda: analysis.open_interactive_chart(self.filepath)).pack(pady=2)
            # Back button to return to main menu
            tk.Button(self.root, text="🔙 Back", bg="#D5DBDB", command=self.main_menu).pack(pady=10)
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.main_menu()

    def _export_chart(self, fig):
        """Export the current matplotlib figure to a PNG file."""
        import tkinter.filedialog as fd
        path = fd.asksaveasfilename(defaultextension='.png', filetypes=[('PNG', '*.png')])
        if not path:
            return
        fig.savefig(path)
        messagebox.showinfo('Export', f'Chart exported to {path}')

    def open_preferences(self):
        """Open a preferences dialog to let users choose timestamp display options."""
        self._clear_window()

        tk.Label(self.root, text="Preferences", font=("Comic Sans MS", 16, "bold"), bg="#AED6F1").pack(pady=10)

        # Timestamp mode selection with explanatory text
        tk.Label(self.root, text="Timestamp display mode:", font=("Arial", 11, "bold"), bg="#AED6F1").pack(anchor='w', padx=10)
        tk.Label(self.root, text="Choose how timestamps are displayed in the app.", fg="#555", bg="#AED6F1").pack(anchor='w', padx=10)
        mode_var = tk.StringVar(value=self.config.get('timestamp_mode', 'local'))
        tk.Radiobutton(self.root, text="Local time", variable=mode_var, value='local', bg="#AED6F1").pack(anchor='w', padx=20)
        tk.Radiobutton(self.root, text="UTC (Coordinated Universal Time)", variable=mode_var, value='utc', bg="#AED6F1").pack(anchor='w', padx=20)
        tk.Radiobutton(self.root, text="Custom format", variable=mode_var, value='custom', bg="#AED6F1").pack(anchor='w', padx=20)
        
        # Timezone selector for world time locations
        tk.Label(self.root, text="Timezone (for explicit selection):", bg="#AED6F1").pack(anchor='w', padx=10, pady=(8,0))
        import utils
        # Timezone selector with optimized autocomplete search
        tk.Label(self.root, text="Timezone (for explicit selection):", bg="#AED6F1").pack(anchor='w', padx=10, pady=(8,0))
        import utils
        
        # Build timezone registry with GMT offsets (cached)
        if not hasattr(self, '_tz_registry'):
            self._tz_registry = utils.build_timezone_registry()
        tz_list_all, tz_display_map = self._tz_registry
        tz_var = tk.StringVar(value=self.config.get('timezone', 'system'))
        
        # Instruction label
        tk.Label(self.root, text="💡 Type city or country name (e.g., 'london', 'tokyo', 'dhaka'):", 
                fg="#666", bg="#AED6F1", font=("Arial", 9)).pack(anchor='w', padx=20, pady=(4, 2))
        
        search_var = tk.StringVar(value='')
        
        # Build a prefix-search index for fast autocomplete (tz_code -> searchable strings)
        search_index = {}
        for tz_code, (display_name, gmt_offset) in tz_display_map.items():
            # Index by lowercase parts: region, city, and full display
            search_keys = [display_name.lower(), gmt_offset.lower(), tz_code.lower()]
            for part in display_name.split('/'):
                search_keys.append(part.lower().strip())
            search_index[tz_code] = search_keys
        
        def get_suggestions(query: str) -> list:
            """Get timezone codes matching the query (prefix or substring match)."""
            if not query:
                return ['system', 'UTC'] + tz_list_all[2:10]  # Return sample list
            
            qlow = query.lower().strip()
            matches = []
            
            # Prefix match first (fastest)
            for tz_code, keys in search_index.items():
                for key in keys:
                    if key.startswith(qlow):
                        matches.append(tz_code)
                        break
            
            # If few matches, try substring match
            if len(matches) < 5:
                for tz_code, keys in search_index.items():
                    if tz_code not in matches:
                        for key in keys:
                            if qlow in key:
                                matches.append(tz_code)
                                break
            
            return matches[:100]  # Limit suggestions to top 100
        
        # Autocomplete dropdown using Combobox
        suggestions_var = tk.StringVar()
        suggestions_combo = ttk.Combobox(self.root, textvariable=suggestions_var, width=50, state='readonly')
        suggestions_combo.pack(anchor='w', padx=20, pady=2)
        
        # Timezone list (Listbox + scrollbar) showing results
        list_frame = tk.Frame(self.root, bg="#AED6F1")
        list_frame.pack(anchor='w', padx=20, pady=(4, 0))
        scrollbar = tk.Scrollbar(list_frame, orient='vertical')
        tz_listbox = tk.Listbox(list_frame, height=6, width=60, yscrollcommand=scrollbar.set)
        scrollbar.config(command=tz_listbox.yview)
        tz_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='left', fill='y')
        
        # Map listbox indices to timezone codes
        self._tz_listbox_map = []
        
        def populate_listbox(tz_codes: list):
            """Populate the listbox with formatted timezone entries."""
            tz_listbox.delete(0, 'end')
            self._tz_listbox_map = []
            for tz_code in tz_codes:
                if tz_code in tz_display_map:
                    display_name, gmt_offset = tz_display_map[tz_code]
                    display_text = f"{display_name} — {gmt_offset}"
                    tz_listbox.insert('end', display_text)
                    self._tz_listbox_map.append(tz_code)
        
        # Update suggestions as user types
        def update_suggestions(*args):
            query = search_var.get()
            sugg = get_suggestions(query)
            sugg_displays = [f"{tz_display_map[tz][0]} — {tz_display_map[tz][1]}" for tz in sugg]
            suggestions_combo['values'] = sugg_displays
            if sugg_displays:
                suggestions_combo.current(0)
                populate_listbox(sugg)
        
        search_var.trace_add('write', update_suggestions)
        
        # When user selects from suggestions, populate listbox with all matching results
        def on_suggestion_select(event=None):
            query = search_var.get()
            if query:
                matches = get_suggestions(query)
                populate_listbox(matches)
        
        suggestions_combo.bind('<<ComboboxSelected>>', on_suggestion_select)
        
        # When user clicks on a listbox item, select that timezone
        def select_from_listbox(event=None):
            sel = tz_listbox.curselection()
            if not sel:
                return
            idx = sel[0]
            if idx < len(self._tz_listbox_map):
                tz_code = self._tz_listbox_map[idx]
                tz_var.set(tz_code)
                update_preview()
        
        tz_listbox.bind('<<ListboxSelect>>', select_from_listbox)
        
        # Initialize listbox with sample timezones
        populate_listbox(['system', 'UTC'] + tz_list_all[2:10])
        # Custom format entry with hint
        tk.Label(self.root, text="Custom strftime format (advanced):", bg="#AED6F1").pack(anchor='w', padx=10)
        custom_entry = tk.Entry(self.root, width=40)
        custom_entry.insert(0, self.config.get('custom_format', '%Y-%m-%d %H:%M:%S %Z'))
        custom_entry.pack(anchor='w', padx=20)
        custom_hint = tk.Label(self.root, text="Enable this by selecting 'Custom format' above. Example tokens: %Y %m %d %H %M %Z", fg="#555", bg="#AED6F1")
        custom_hint.pack(anchor='w', padx=20)

        # Relative time checkbox
        rel_var = tk.BooleanVar(value=self.config.get('show_relative', True))
        tk.Checkbutton(self.root, text="Show relative time (e.g., '2h ago')", variable=rel_var, bg="#AED6F1").pack(anchor='w', padx=10)

        # Enable/disable custom entry based on selection
        def update_custom_visibility(*args):
            if mode_var.get() == 'custom':
                custom_entry.config(state='normal')
                custom_hint.config(fg="#333")
            else:
                custom_entry.config(state='disabled')
                custom_hint.config(fg="#AAA")

        # Bind the update visibility
        mode_var.trace_add('write', update_custom_visibility)
        # Initialize state
        update_custom_visibility()
        # Live preview area
        tk.Label(self.root, text="Preview:", font=("Arial", 11, "bold"), bg="#AED6F1").pack(anchor='w', pady=(10,0), padx=10)
        preview_label = tk.Label(self.root, text="", bg="#FFFFFF", anchor='w', relief='solid', width=55)
        preview_label.pack(anchor='w', padx=20, pady=5)

        # Deterministic sample for preview to make behavior easy to understand
        sample_iso = '2026-01-03T12:00:00+00:00'
        self.pref_mode_var = mode_var
        self.pref_custom_entry = custom_entry
        self.pref_rel_var = rel_var
        self.pref_preview_label = preview_label
        self.pref_sample_iso = sample_iso
        self.pref_tz_var = tz_var

        def update_preview(*args):
            mode = mode_var.get()
            custom_fmt = custom_entry.get()
            show_rel = bool(rel_var.get())
            tz = tz_var.get()
            from utils import format_iso_timestamp
            preview_text = format_iso_timestamp(sample_iso, mode=mode, custom_fmt=custom_fmt, show_relative=show_rel, tz_name=tz)
            preview_label.config(text=preview_text)

        # Bind updates
        mode_var.trace_add('write', update_preview)
        rel_var.trace_add('write', update_preview)
        tz_var.trace_add('write', update_preview)
        custom_entry.bind('<KeyRelease>', lambda e: update_preview())


        def update_preview(*args):
            mode = mode_var.get()
            custom_fmt = custom_entry.get()
            show_rel = bool(rel_var.get())
            tz = tz_var.get()
            from utils import format_iso_timestamp
            preview_text = format_iso_timestamp(sample_iso, mode=mode, custom_fmt=custom_fmt, show_relative=show_rel, tz_name=tz)
            preview_label.config(text=preview_text)

        # Expose update helper for tests and immediate updates
        self._update_preferences_preview = update_preview

        # Bind updates
        mode_var.trace_add('write', update_preview)
        rel_var.trace_add('write', update_preview)
        tz_var.trace_add('write', update_preview)
        custom_entry.bind('<KeyRelease>', lambda e: update_preview())

        # Initialize preview
        update_preview()

        # Save and Back controls (placed after preview to ensure they are visible)
        def save_prefs():
            self.config['timestamp_mode'] = mode_var.get()
            self.config['custom_format'] = custom_entry.get()
            self.config['show_relative'] = bool(rel_var.get())
            self.config['timezone'] = tz_var.get()
            import config as _c
            _c.save_config(self.config)
            messagebox.showinfo("Preferences", "Preferences saved.")
            self.main_menu()

        tk.Button(self.root, text="Save", bg="#58D68D", fg="white", command=save_prefs).pack(pady=5)
        tk.Frame(self.root, bg="#AED6F1").pack(pady=2)  # spacer
        tk.Button(self.root, text="🔙 Back", bg="#D5DBDB", command=self.main_menu).pack(side='left', padx=20)
        tk.Button(self.root, text="Cancel", bg="#EC7063", fg="white", command=self.main_menu).pack()

        tk.Label(self.root, text="© 2025 IODEX. All rights reserved.", 
                bg="#AED6F1", font=("Arial", 9, "italic")).pack(side="bottom", pady=5)

    @staticmethod
    def compute_preview_text(sample_iso: str, mode: str, custom_fmt: str, show_rel: bool, tz_name: str = 'system') -> str:
        """Return the preview text without creating GUI elements (used by tests)."""
        from utils import format_iso_timestamp
        return format_iso_timestamp(sample_iso, mode=mode, custom_fmt=custom_fmt, show_relative=show_rel, tz_name=tz_name)
    
    def reset_expenses(self):
        """Clear all expense records after user confirmation."""
        if messagebox.askyesno("Reset", "Are you sure you want to delete all expenses?"):
            storage.clear_expenses(self.filepath)
            messagebox.showinfo("Reset", "All expenses have been deleted.")
            self.main_menu()

    def _on_exit(self):
        """Save config and exit cleanly."""
        import config
        config.save_config(self.config)
        self.root.quit()


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
