import tkinter as tk
from tkinter import ttk

class ApartmentListPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        label = tk.Label(self, text="Apartment Inventory", font=("Arial", 18, "bold"))
        label.pack(pady=10)

        # --- Search Section ---
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(search_frame, text="Filter by City:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        
        search_btn = tk.Button(search_frame, text="Search", command=self.filter_apartments)
        search_btn.pack(side="left")

        # --- Table Section (Treeview) ---
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Define Columns
        columns = ("id", "location", "type", "rent", "rooms", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Define Headings
        self.tree.heading("id", text="ID")
        self.tree.heading("location", text="City")
        self.tree.heading("type", text="Type")
        self.tree.heading("rent", text="Rent (£)")
        self.tree.heading("rooms", text="Rooms")
        self.tree.heading("status", text="Status")

        # Column Widths
        self.tree.column("id", width=50)
        self.tree.column("status", width=100)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Buttons at the bottom
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Refresh List", command=self.load_data).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Edit Selected", command=self.go_to_edit).pack(side="left", padx=10)

    def load_data(self):
        # This will eventually fetch data from MySQL
        print("Refreshing apartment list...")
        # For now, let's add a dummy row for UI testing
        self.tree.insert("", "end", values=("1", "Bristol", "2-Bedroom", "1200", "3", "Available"))

    def filter_apartments(self):
        city = self.search_entry.get()
        print(f"Searching for apartments in: {city}")