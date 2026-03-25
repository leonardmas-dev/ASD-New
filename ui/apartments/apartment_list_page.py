import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Fix for "ModuleNotFoundError"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from backend.apartment_service import get_all_apartments

class ApartmentListPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Apartment Inventory", font=("Arial", 18, "bold")).pack(pady=10)

        # --- Search Section ---
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(search_frame, text="Filter by City:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        
        tk.Button(search_frame, text="Search", command=self.filter_apartments).pack(side="left")

        # --- Table Section (Treeview) ---
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("id", "location", "type", "rent", "rooms", "status")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        # Headings
        self.tree.heading("id", text="ID")
        self.tree.heading("location", text="City")
        self.tree.heading("type", text="Type")
        self.tree.heading("rent", text="Rent (£)")
        self.tree.heading("rooms", text="Rooms")
        self.tree.heading("status", text="Status")

        # Layout
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Action Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Refresh List", command=self.load_data, width=15).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Edit Selected", command=self.go_to_edit, width=15, bg="#3498db", fg="white").pack(side="left", padx=10)

        # Initial Load
        self.load_data()

    def load_data(self):
        """Fetches data from MySQL and populates the table"""
        # Clear current table
        for item in self.tree.get_children():
            self.tree.delete(item)

        apartments = get_all_apartments()
        id_to_city = {1: "Bristol", 2: "Cardiff", 3: "London", 4: "Manchester"}

        for apt in apartments:
            city_name = id_to_city.get(apt['location_id'], "Unknown")
            # Logic to show friendly status text
            status_text = "Available" if apt['is_available'] == 1 else "Occupied"
            
            self.tree.insert("", "end", values=(
                apt['apartment_id'],
                city_name,
                apt['apartment_type'],
                f"£{apt['monthly_rent']}",
                apt['num_rooms'],
                status_text
            ))

    def filter_apartments(self):
        query = self.search_entry.get().lower()
        self.load_data() # Reset list first
        if not query: return

        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if query not in str(values[1]).lower():
                self.tree.detach(item)

    def go_to_edit(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection", "Please select an apartment to edit.")
            return
        
        apt_data = self.tree.item(selected_item)['values']
        # This will send the ID to the main controller to open the Edit Page
        if self.controller:
            self.controller.show_edit_apartment(apt_data[0])