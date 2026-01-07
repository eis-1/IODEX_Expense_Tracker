"""
GUI module for IODEX Expense Tracker.
Handles all user interface rendering and interaction logic.
"""

import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
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
        
        # Larger default size for better data table visibility
        self.root.geometry("1100x700")
        
        # Allow resizing for user flexibility
        self.root.resizable(True, True)
        
        # Set minimum size to prevent layout breaking
        self.root.minsize(800, 600)
        
        # Center window on screen
        self._center_window()

        # Cache for background image to avoid reloading
        self._bg_image = None
        self.background_label = self._setup_background()
        
        # Bind resize event to update background
        self.root.bind('<Configure>', self._on_window_resize)

        # Category options
        self.categories = ["Food", "Rent", "Utilities", "Shopping"]
        
        # Common widget styling - define once for performance
        self.button_font = ("Arial", 11)
        self.title_font = ("Comic Sans MS", 18, "bold")
        self.label_font = ("Arial", 12)
        self.input_font = ("Arial", 11)
        
        # Track resize to avoid excessive redraws
        self._resize_job = None

        # Migration prompt: only run when using the default storage path
        import os

        if filepath == DEFAULT_FILENAME:
            txt_path = "expenses.txt"
            db_path = "expenses.db"
            if os.path.exists(txt_path) and not os.path.exists(db_path):
                self._show_migration_prompt(txt_path, db_path)
            else:
                # If DB exists, switch default to DB
                if os.path.exists(db_path):
                    self.filepath = db_path
                self.main_menu()
        else:
            # Non-default filepath provided (e.g., tests pass temp files) — don't prompt or auto-migrate
            self.main_menu()

    def _show_migration_prompt(self, txt_path, db_path):
        def migrate():
            try:
                from import_export import migrate_legacy_to_db

                migrate_legacy_to_db(src_path=txt_path, db_path=db_path)
                self.filepath = db_path
                tk.messagebox.showinfo(
                    "Migration",
                    f"Expenses migrated to '{db_path}'. App will now use the database.",
                )
            except Exception as e:
                tk.messagebox.showerror("Migration Failed", str(e))
            self.main_menu()

        self._clear_window()
        tk.Label(
            self.root,
            text="Migrate to Database?",
            font=("Comic Sans MS", 16, "bold"),
            bg="#AED6F1",
        ).pack(pady=30)
        tk.Label(
            self.root,
            text="A legacy expenses.txt file was found. Would you like to migrate your data to the new, faster expenses.db database?",
            wraplength=600,
            bg="#AED6F1",
            font=("Arial", 12),
        ).pack(pady=10)
        tk.Button(
            self.root,
            text="Migrate Now",
            bg="#58D68D",
            fg="white",
            command=migrate,
            font=("Arial", 12),
        ).pack(pady=8)
        tk.Button(
            self.root,
            text="Skip",
            bg="#EC7063",
            fg="white",
            command=self.main_menu,
            font=("Arial", 12),
        ).pack(pady=8)
        self._add_footer()
    
    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def _on_window_resize(self, event):
        """Handle window resize events to update background smoothly."""
        # Only respond to root window resize events
        if event.widget != self.root:
            return
        
        # Debounce resize events to avoid excessive redraws
        if self._resize_job:
            self.root.after_cancel(self._resize_job)
        
        self._resize_job = self.root.after(100, self._update_background_size)
    
    def _update_background_size(self):
        """Update background to match current window size."""
        if self.background_label and self.background_label.winfo_exists():
            # Background already uses relwidth/relheight so it scales automatically
            pass
        self._resize_job = None

    def _setup_background(self):
        """
        Setup background image or solid color fallback.
        Background scales with window size for responsive design.

        Returns:
            Label widget containing the background
        """
        try:
            # Use resource_path so the image can be found when running from a PyInstaller bundle
            from utils import resource_path

            img_path = resource_path("photo1.jpg")
            # Load original image (will scale via Canvas or use solid color)
            base_image = Image.open(img_path)
            
            # Get current window size
            self.root.update_idletasks()
            width = max(self.root.winfo_width(), 700)
            height = max(self.root.winfo_height(), 500)
            
            # Resize to current window size
            image = base_image.resize((width, height), Image.Resampling.LANCZOS)
            self._bg_image = ImageTk.PhotoImage(image)
            
            background_label = tk.Label(self.root, image=self._bg_image)
            background_label.image = self._bg_image  # Keep a reference
        except Exception as e:
            print("Background image error:", e)
            # Solid color fallback - modern gradient-like color
            background_label = tk.Label(self.root, bg="#E8F4F8")
        
        background_label.place(x=0, y=0, relwidth=1, relheight=1)
        return background_label

    def _clear_window(self):
        """Remove all widgets except the background label."""
        for widget in self.root.winfo_children():
            if widget != self.background_label:
                widget.destroy()

    def _add_footer(self):
        """Add copyright footer to the current window."""
        tk.Label(
            self.root,
            text="© 2025 IODEX. All rights reserved.",
            bg="#B3E5FC",
            font=("Arial", 9, "italic"),
        ).pack(side="bottom", pady=5)
    
    def _create_button(self, text, bg_color, command, width=35, pady=6):
        """Create a standardized button with consistent styling.
        
        Args:
            text: Button text
            bg_color: Background color
            command: Command to execute
            width: Button width (default: 35)
            pady: Vertical padding (default: 6)
        
        Returns:
            Button widget
        """
        btn = tk.Button(
            self.root,
            text=text,
            width=width,
            bg=bg_color,
            font=self.button_font,
            command=command,
            cursor="hand2",
            relief="raised",
            bd=2,
            padx=10,
            pady=8
        )
        btn.pack(pady=pady)
        return btn

    def main_menu(self):
        """Display the main menu screen."""
        self._clear_window()

        tk.Label(
            self.root,
            text="🧾 Expense Tracker Menu",
            font=self.title_font,
            bg="#76D7C4",
        ).pack(pady=50)

        # Use optimized button creation
        # Note: Save button removed - all data is saved automatically
        menu_buttons = [
            ("➕ Add Expense", "#A3E4D7", self.add_expense_menu),
            ("📄 View All Expenses", "#F9E79F", self.view_expenses),
            ("📊 Analyze Expenses", "#D2B4DE", self.analyze_expenses),
            ("🗑 Reset Expenses", "#F5B7B1", self.reset_expenses),
            ("⚙ Preferences", "#FAD7A0", self.open_preferences),
            ("❌ Exit", "#D7DBDD", self._on_exit),
        ]
        
        for text, color, cmd in menu_buttons:
            self._create_button(text, color, cmd)

        self._add_footer()

    def add_expense_menu(self):
        """Display the category selection menu for adding expenses."""
        self._clear_window()

        tk.Label(
            self.root,
            text="Choose a Category",
            font=self.title_font,
            bg="#AED6F1",
        ).pack(pady=20)

        # Create category buttons with better spacing
        for cat in self.categories:
            tk.Button(
                self.root,
                text=cat,
                width=25,
                font=self.button_font,
                bg="#85C1E9",
                cursor="hand2",
                relief="raised",
                bd=2,
                padx=10,
                pady=8,
                command=lambda c=cat: self.category_input(c),
            ).pack(pady=5)

        # Back button with better styling
        tk.Button(
            self.root,
            text="🔙 Back",
            width=25,
            bg="#D5DBDB",
            font=self.button_font,
            cursor="hand2",
            command=self.main_menu
        ).pack(pady=15)

        tk.Label(
            self.root,
            text="© 2025 IODEX. All rights reserved.",
            bg="#AED6F1",
            font=("Arial", 9, "italic"),
        ).pack(side="bottom", pady=5)

    def category_input(self, category):
        """
        Display the input form for a specific expense category.

        Args:
            category: The selected expense category
        """
        self._clear_window()

        # Title with better spacing
        tk.Label(
            self.root,
            text=f"Enter {category} Expense",
            font=self.title_font,
            bg="#AED6F1",
        ).pack(pady=30)

        # Amount input with larger, more accessible fields
        tk.Label(
            self.root,
            text="Amount:",
            bg="#AED6F1",
            font=self.label_font
        ).pack(pady=(15, 5))
        
        amount_entry = tk.Entry(
            self.root,
            font=self.input_font,
            width=30,
            relief="solid",
            bd=2
        )
        amount_entry.pack(pady=5)
        amount_entry.focus()  # Auto-focus for better UX

        # Description input
        tk.Label(
            self.root,
            text="Description:",
            bg="#AED6F1",
            font=self.label_font
        ).pack(pady=(15, 5))
        
        description_entry = tk.Entry(
            self.root,
            font=self.input_font,
            width=30,
            relief="solid",
            bd=2
        )
        description_entry.pack(pady=5)
        
        # Bind Enter key for quick submission
        def on_enter(event):
            self._save_expense_wrapper(
                category, amount_entry.get(), description_entry.get()
            )
        
        amount_entry.bind('<Return>', on_enter)
        description_entry.bind('<Return>', on_enter)

        # Action buttons with better styling
        button_frame = tk.Frame(self.root, bg="#AED6F1")
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="✅ Save",
            bg="#58D68D",
            fg="white",
            font=self.button_font,
            width=12,
            padx=10,
            pady=8,
            cursor="hand2",
            command=lambda: self._save_expense_wrapper(
                category, amount_entry.get(), description_entry.get()
            ),
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="❌ Cancel",
            bg="#EC7063",
            fg="white",
            font=self.button_font,
            width=12,
            padx=10,
            pady=8,
            cursor="hand2",
            command=self.main_menu,
        ).pack(side="left", padx=5)

        self._add_footer()

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

        tk.Label(
            self.root,
            text="--- All Expenses ---",
            font=self.title_font,
            bg="#AED6F1",
        ).pack(pady=15)

        # Create frame for better layout control.
        # NOTE: Tests look for a widget under root with a Treeview-like API
        # (get_children/item). This proxy frame delegates those calls to the
        # real Treeview so tests can find it even though we nest the Treeview.
        class _TreeviewProxyFrame(tk.Frame):
            def __init__(self, master, **kwargs):
                super().__init__(master, **kwargs)
                self._tree: ttk.Treeview | None = None

            def get_children(self, *args, **kwargs):
                if self._tree is None:
                    return ()
                return self._tree.get_children(*args, **kwargs)

            def item(self, *args, **kwargs):
                if self._tree is None:
                    return {}
                return self._tree.item(*args, **kwargs)

        # Create scrollbars and Treeview inside the proxy frame
        # (the Treeview itself remains the source of truth)
        tree_frame = _TreeviewProxyFrame(self.root, bg="#AED6F1")
        tree_frame.pack(expand=True, fill="both", padx=20, pady=10)

        # Add scrollbars
        v_scrollbar = tk.Scrollbar(tree_frame, orient="vertical")
        h_scrollbar = tk.Scrollbar(tree_frame, orient="horizontal")

        columns = ("Category", "Amount", "Description", "Timestamp")
        tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
        )
        tree_frame._tree = tree
        
        v_scrollbar.config(command=tree.yview)
        h_scrollbar.config(command=tree.xview)

        # Set column widths and headings for better visibility
        tree.heading("Category", text="Category")
        tree.heading("Amount", text="Amount")
        tree.heading("Description", text="Description")
        tree.heading("Timestamp", text="Timestamp")
        
        tree.column("Category", width=100, minwidth=80)
        tree.column("Amount", width=100, minwidth=80)
        tree.column("Description", width=200, minwidth=150)
        tree.column("Timestamp", width=300, minwidth=250)  # Wider for full timestamps
        
        # Pack scrollbars and tree
        tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        # Load and display expenses
        import utils

        expenses = storage.load_expenses(self.filepath)
        for category, amount, description, *rest in expenses:
            timestamp = rest[0] if rest else ""
            # Format timestamp according to user's preference for display
            mode = self.config.get("timestamp_mode", "local")
            custom_fmt = self.config.get("custom_format", "%Y-%m-%d %H:%M:%S %Z")
            show_rel = bool(self.config.get("show_relative", True))
            ts_display = (
                utils.format_iso_timestamp(
                    timestamp, mode=mode, custom_fmt=custom_fmt, show_relative=show_rel
                )
                if timestamp
                else ""
            )
            # Store raw timestamp in tags for accurate deletion
            item_id = tree.insert(
                "", tk.END, values=(category, f"${amount:.2f}", description, ts_display),
                tags=(timestamp,)  # Store raw timestamp as tag
            )

        total = storage.get_total_spent(self.filepath)
        tk.Label(
            self.root,
            text=f"💰 Total Spent: ${total:.2f}",
            font=self.label_font,
            bg="#AED6F1",
        ).pack(pady=10)

        # Button frame for better layout
        button_frame = tk.Frame(self.root, bg="#AED6F1")
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame,
            text="🗑️ Delete Selected",
            bg="#F5B7B1",
            font=self.button_font,
            width=20,
            padx=10,
            pady=6,
            cursor="hand2",
            command=lambda: self._delete_selected(tree),
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame,
            text="🔙 Back",
            bg="#D5DBDB",
            font=self.button_font,
            width=20,
            padx=10,
            pady=6,
            cursor="hand2",
            command=self.main_menu
        ).pack(side="left", padx=5)

        self._add_footer()

    def _delete_selected(self, tree: ttk.Treeview):
        """Delete the selected rows from storage after confirmation.

        This method handles CSV-based storage deletion by identifying the expense
        from the tree values (category, $amount, description, timestamp).
        """
        selected = tree.selection()
        if not selected:
            messagebox.showinfo(
                "Delete", "Please select one or more expenses to delete."
            )
            return

        if not messagebox.askyesno(
            "Delete", "Are you sure you want to delete the selected expense(s)?"
        ):
            return

        deleted_any = False
        for item in selected:
            vals = tree.item(item)["values"]
            tags = tree.item(item)["tags"]
            
            # Expect values: (category, '$amount', description, formatted_timestamp)
            category = vals[0]
            amount_str = str(vals[1]).lstrip("$").replace(",", "")
            try:
                amount = float(amount_str)
            except Exception:
                continue
            description = vals[2]
            
            # Get raw timestamp from tags (not the formatted display value)
            timestamp = tags[0] if tags and tags[0] else None
            
            if storage.delete_expense(
                category, amount, description, timestamp, path=self.filepath
            ):
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
            # Show a friendly message but keep a Back button on the analyze screen
            tk.Label(
                self.root,
                text="No expenses to analyze.",
                font=("Comic Sans MS", 14, "normal"),
                bg="#AED6F1",
            ).pack(pady=20)
            tk.Button(
                self.root, text="🔙 Back", bg="#D5DBDB", command=self.main_menu
            ).pack(pady=10)
            self._add_footer()
            return

        try:
            fig = analysis.create_category_chart(self.filepath)

            # Lazy import matplotlib to speed up startup
            from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.draw()
            canvas.get_tk_widget().pack(pady=20)

            tk.Button(
                self.root,
                text="⬇ Export Image",
                bg="#AED6F1",
                command=lambda: self._export_chart(fig),
            ).pack(pady=2)
            tk.Button(
                self.root,
                text="🌐 Open Interactive Chart",
                bg="#AED6F1",
                command=lambda: analysis.open_interactive_chart(self.filepath),
            ).pack(pady=2)
            # Back button to return to main menu
            tk.Button(
                self.root, text="🔙 Back", bg="#D5DBDB", command=self.main_menu
            ).pack(pady=10)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.main_menu()

    def _export_chart(self, fig):
        """Export the current matplotlib figure to a PNG file."""
        import tkinter.filedialog as fd

        path = fd.asksaveasfilename(
            defaultextension=".png", filetypes=[("PNG", "*.png")]
        )
        if not path:
            return
        fig.savefig(path)
        messagebox.showinfo("Export", f"Chart exported to {path}")

    def open_preferences(self):
        """Open a preferences dialog to let users choose timestamp display options."""
        self._clear_window()

        # Create a scrollable frame for the content
        canvas = tk.Canvas(self.root, bg="#AED6F1", highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg="#AED6F1")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Title
        tk.Label(
            scrollable_frame,
            text="⚙️ Preferences",
            font=("Comic Sans MS", 16, "bold"),
            bg="#AED6F1",
        ).pack(pady=15, padx=10)

        # === SECTION 1: Timestamp Mode ===
        tk.Label(
            scrollable_frame,
            text="1. Timestamp Display Mode",
            font=("Arial", 12, "bold"),
            fg="#1a5490",
            bg="#AED6F1",
        ).pack(anchor="w", padx=15, pady=(10, 5))
        tk.Label(
            scrollable_frame,
            text="Choose how timestamps appear in the app.",
            fg="#555",
            bg="#AED6F1",
            font=("Arial", 9),
        ).pack(anchor="w", padx=20, pady=(0, 5))

        mode_var = tk.StringVar(value=self.config.get("timestamp_mode", "local"))
        tk.Radiobutton(
            scrollable_frame,
            text="📍 Local time (your timezone)",
            variable=mode_var,
            value="local",
            bg="#AED6F1",
        ).pack(anchor="w", padx=30)
        tk.Radiobutton(
            scrollable_frame,
            text="🌍 UTC (Coordinated Universal Time)",
            variable=mode_var,
            value="utc",
            bg="#AED6F1",
        ).pack(anchor="w", padx=30)
        tk.Radiobutton(
            scrollable_frame,
            text="✏️ Custom format (advanced)",
            variable=mode_var,
            value="custom",
            bg="#AED6F1",
        ).pack(anchor="w", padx=30)

        # === SECTION 2: Timezone Selection ===
        tk.Label(
            scrollable_frame,
            text="2. Timezone Selection",
            font=("Arial", 12, "bold"),
            fg="#1a5490",
            bg="#AED6F1",
        ).pack(anchor="w", padx=15, pady=(15, 5))
        tk.Label(
            scrollable_frame,
            text="💡 Search by city name (e.g., 'london', 'tokyo', 'dhaka'):",
            fg="#666",
            bg="#AED6F1",
            font=("Arial", 9),
        ).pack(anchor="w", padx=20, pady=(0, 5))

        import utils

        if not hasattr(self, "_tz_registry"):
            self._tz_registry = utils.build_timezone_registry()
        tz_list_all, tz_display_map = self._tz_registry
        tz_var = tk.StringVar(value=self.config.get("timezone", "system"))

        # Search input
        search_var = tk.StringVar(value="")
        search_entry = tk.Entry(
            scrollable_frame, textvariable=search_var, width=50, font=("Arial", 10)
        )
        search_entry.pack(anchor="w", padx=20, pady=(0, 5))

        # Build search index
        search_index = {}
        for tz_code, (display_name, gmt_offset) in tz_display_map.items():
            search_keys = [display_name.lower(), gmt_offset.lower(), tz_code.lower()]
            for part in display_name.split("/"):
                search_keys.append(part.lower().strip())
            search_index[tz_code] = search_keys

        def get_suggestions(query: str) -> list:
            """Get timezone codes matching the query."""
            if not query:
                return ["system", "UTC"] + tz_list_all[2:15]

            qlow = query.lower().strip()
            matches = []
            for tz_code, keys in search_index.items():
                for key in keys:
                    if key.startswith(qlow) or qlow in key:
                        matches.append(tz_code)
                        break
            return matches[:50]

        # Timezone listbox (now shows City, Country — GMT+X format)
        list_frame = tk.Frame(scrollable_frame, bg="#AED6F1")
        list_frame.pack(anchor="w", padx=20, pady=(0, 5), fill="both", expand=True)

        list_scrollbar = tk.Scrollbar(list_frame, orient="vertical")
        tz_listbox = tk.Listbox(
            list_frame,
            height=6,
            width=70,
            yscrollcommand=list_scrollbar.set,
            font=("Arial", 9),
            bg="#FFFFFF",
        )
        list_scrollbar.config(command=tz_listbox.yview)
        tz_listbox.pack(side="left", fill="both", expand=True)
        list_scrollbar.pack(side="right", fill="y")

        self._tz_listbox_map = []

        def populate_listbox(tz_codes: list):
            """Populate listbox with City, Country — GMT format."""
            tz_listbox.delete(0, "end")
            self._tz_listbox_map = []
            for tz_code in tz_codes:
                if tz_code in tz_display_map:
                    display_name, gmt_offset = tz_display_map[tz_code]
                    # Extract just the city part (last component)
                    city = display_name.split("/")[-1]
                    country = (
                        display_name.split("/")[0] if "/" in display_name else "System"
                    )
                    # Format: City, Country — GMT offset
                    display_text = f"{city}, {country} — {gmt_offset}"
                    tz_listbox.insert("end", display_text)
                    self._tz_listbox_map.append(tz_code)

        def update_suggestions(*args):
            query = search_var.get()
            sugg = get_suggestions(query)
            populate_listbox(sugg)

        search_var.trace_add("write", update_suggestions)

        def select_from_listbox(event=None):
            sel = tz_listbox.curselection()
            if not sel:
                return
            idx = sel[0]
            if idx < len(self._tz_listbox_map):
                tz_code = self._tz_listbox_map[idx]
                tz_var.set(tz_code)
                update_preview()

        tz_listbox.bind("<<ListboxSelect>>", select_from_listbox)
        populate_listbox(["system", "UTC"] + tz_list_all[2:15])

        # === SECTION 3: Custom Format ===
        tk.Label(
            scrollable_frame,
            text="3. Custom Time Format (Advanced)",
            font=("Arial", 12, "bold"),
            fg="#1a5490",
            bg="#AED6F1",
        ).pack(anchor="w", padx=15, pady=(15, 5))
        tk.Label(
            scrollable_frame,
            text="Available tokens: %Y (year) %m (month) %d (day) %H (hour) %M (min) %Z (zone)",
            fg="#555",
            bg="#AED6F1",
            font=("Arial", 8),
        ).pack(anchor="w", padx=20, pady=(0, 3))

        custom_entry = tk.Entry(scrollable_frame, width=50, font=("Arial", 10))
        custom_entry.insert(0, self.config.get("custom_format", "%Y-%m-%d %H:%M:%S %Z"))
        custom_entry.pack(anchor="w", padx=20, pady=(0, 5))

        # === SECTION 4: Options ===
        tk.Label(
            scrollable_frame,
            text="4. Display Options",
            font=("Arial", 12, "bold"),
            fg="#1a5490",
            bg="#AED6F1",
        ).pack(anchor="w", padx=15, pady=(15, 5))

        rel_var = tk.BooleanVar(value=self.config.get("show_relative", True))
        tk.Checkbutton(
            scrollable_frame,
            text="⏱️ Show relative time (e.g., '2h ago')",
            variable=rel_var,
            bg="#AED6F1",
            font=("Arial", 10),
        ).pack(anchor="w", padx=20)

        # === SECTION 5: Live Preview ===
        tk.Label(
            scrollable_frame,
            text="5. Preview",
            font=("Arial", 12, "bold"),
            fg="#1a5490",
            bg="#AED6F1",
        ).pack(anchor="w", padx=15, pady=(15, 5))

        preview_label = tk.Label(
            scrollable_frame,
            text="",
            bg="#FFFFFF",
            anchor="w",
            relief="solid",
            wraplength=600,
            justify="left",
            font=("Arial", 10),
            padx=10,
            pady=8,
        )
        preview_label.pack(anchor="w", padx=20, pady=(0, 10), fill="x")

        # Bindings for updates
        def update_custom_visibility(*args):
            custom_entry.config(
                state="normal" if mode_var.get() == "custom" else "disabled"
            )

        sample_iso = "2026-01-03T12:00:00+00:00"

        def update_preview(*args):
            mode = mode_var.get()
            custom_fmt = custom_entry.get()
            show_rel = bool(rel_var.get())
            tz = tz_var.get()
            from utils import format_iso_timestamp

            preview_text = format_iso_timestamp(
                sample_iso,
                mode=mode,
                custom_fmt=custom_fmt,
                show_relative=show_rel,
                tz_name=tz,
            )
            preview_label.config(text=f"Sample: {preview_text}")

        mode_var.trace_add("write", update_custom_visibility)
        mode_var.trace_add("write", update_preview)
        rel_var.trace_add("write", update_preview)
        tz_var.trace_add("write", update_preview)
        custom_entry.bind("<KeyRelease>", lambda e: update_preview())

        update_custom_visibility()
        update_preview()

        # === ACTION BUTTONS (Fixed at bottom) ===
        button_frame = tk.Frame(self.root, bg="#AED6F1")
        button_frame.pack(side="bottom", fill="x", padx=20, pady=10)

        def save_prefs():
            self.config["timestamp_mode"] = mode_var.get()
            self.config["custom_format"] = custom_entry.get()
            self.config["show_relative"] = bool(rel_var.get())
            self.config["timezone"] = tz_var.get()
            import config as _c

            _c.save_config(self.config)
            messagebox.showinfo("Preferences", "✅ Preferences saved successfully!")
            self.main_menu()

        tk.Button(
            button_frame,
            text="💾 Save",
            bg="#58D68D",
            fg="white",
            command=save_prefs,
            font=("Arial", 11),
            padx=20,
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame,
            text="🔙 Back",
            bg="#D5DBDB",
            command=self.main_menu,
            font=("Arial", 11),
            padx=20,
        ).pack(side="left", padx=5)
        tk.Button(
            button_frame,
            text="❌ Cancel",
            bg="#EC7063",
            fg="white",
            command=self.main_menu,
            font=("Arial", 11),
            padx=20,
        ).pack(side="left", padx=5)

        tk.Label(
            self.root,
            text="© 2025 IODEX. All rights reserved.",
            bg="#AED6F1",
            font=("Arial", 8, "italic"),
        ).pack(side="bottom", pady=3)

        # Store references for backward compatibility with tests
        self.pref_mode_var = mode_var
        self.pref_custom_entry = custom_entry
        self.pref_rel_var = rel_var
        self.pref_tz_var = tz_var
        self._update_preferences_preview = update_preview

    @staticmethod
    def compute_preview_text(
        sample_iso: str,
        mode: str,
        custom_fmt: str,
        show_rel: bool,
        tz_name: str = "system",
    ) -> str:
        """Return the preview text without creating GUI elements (used by tests)."""
        from utils import format_iso_timestamp

        return format_iso_timestamp(
            sample_iso,
            mode=mode,
            custom_fmt=custom_fmt,
            show_relative=show_rel,
            tz_name=tz_name,
        )

    def reset_expenses(self):
        """Clear all expense records after user confirmation."""
        if messagebox.askyesno(
            "Reset", "Are you sure you want to delete all expenses?"
        ):
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
    ExpenseTrackerGUI(root, filepath)
    root.mainloop()


if __name__ == "__main__":
    run_application()
