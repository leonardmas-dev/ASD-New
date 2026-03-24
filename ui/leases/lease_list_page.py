import tkinter as tk
from tkinter import ttk

class LeaseListPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        label = tk.Label(self, text="Active Lease Agreements", font=("Arial", 18, "bold"))
        label.pack(pady=10)

        # --- Search Section ---
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(search_frame, text="Search by Tenant NI:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        
        search_btn = tk.Button(search_frame, text="Find Lease", command=self.filter_leases)
        search_btn.pack(side="left")

        # --- Table Section (Treeview) ---
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Define Columns for Lease tracking
        columns = ("id", "tenant", "apartment", "start", "end", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Define Headings
        self.tree.heading("id", text="Lease ID")
        self.tree.heading("tenant", text="Tenant (NI)")
        self.tree.heading("apartment", text="Apt ID")
        self.tree.heading("start", text="Start Date")
        self.tree.heading("end", text="End Date")
        self.tree.heading("status", text="Status")

        # Set Column Widths
        self.tree.column("id", width=70)
        self.tree.column("status", width=100)

        # Add Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bottom Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Refresh Leases", command=self.load_leases).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Manage/Terminate Selected", 
                  bg="#e67e22", fg="white", command=self.go_to_edit_lease).pack(side="left", padx=10)

    def load_leases(self):
        # This will eventually fetch from the 'leases' table in MySQL
        print("Fetching lease records...")
        # Dummy data for UI preview
        self.tree.insert("", "end", values=("L-101", "AB123456C", "APT-4B", "2025-01-01", "2026-01-01", "Active"))

    def filter_leases(self):
        ni_number = self.search_entry.get()
        print(f"Searching for leases for NI: {ni_number}")

    def go_to_edit_lease(self):
        selected = self.tree.focus()
        if selected:
            # Logic to pass data to edit_lease_page.py
            self.controller.show_frame("EditLeasePage")
        else:
            from tkinter import messagebox
            messagebox.showwarning("Selection Error", "Please select a lease to manage.")