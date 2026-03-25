import sys
import os

# Fix for "ModuleNotFoundError": 
# Adds the project root directory to the python path so it can find 'backend'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import tkinter as tk
from tkinter import ttk, messagebox
# Now this import will work because of the sys.path lines above
from backend.apartment_service import get_all_apartments

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

        # Auto-load data when the page opens
        self.load_data()

    def load_data(self):
        """Fetches data from MySQL and populates the table"""
        # 1. Clear current table data
        for item in self.tree.get_children():
            self.tree.delete(item)

        # 2. Get data from backend
        apartments = get_all_apartments()
        
        # 3. Map IDs back to names for the UI
        id_to_city = {1: "Bristol", 2: "Cardiff", 3: "London", 4: "Manchester"}

        # 4. Insert rows into Treeview
        for apt in apartments:
            city_name = id_to_city.get(apt['location_id'], "Unknown")
            # Using your MySQL column names from the screenshot
            status_text = "Available" if apt['is_available'] == 1 else "Occupied"
            
            self.tree.insert("", "end", values=(
                apt['apartment_id'],
                city_name,
                apt['apartment_type'],
                f"£{apt['monthly_rent']}",
                apt['num_rooms'],
                status_text
            ))
        print("UI: Apartment list refreshed from MySQL.")

    def filter_apartments(self):
        city_query = self.search_entry.get().lower()
        # Simple UI filtering: hide rows that don't match the search
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if city_query not in str(values[1]).lower():
                self.tree.detach(item) # Temporarily hide
            else:
                self.tree.move(item, '', 'end') # Show

    def go_to_edit(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showwarning("Selection", "Please select an apartment to edit.")
            return
        
        apt_id = self.tree.item(selected_item)['values'][0]
        print(f"Opening Edit Page for Apartment ID: {apt_id}")

# --- TEST RUN BLOCK ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Inventory List Test")
    root.geometry("800x500")
    
    # Passing None for controller since we are testing this page in isolation
    page = ApartmentListPage(root, None)
    page.pack(expand=True, fill="both")
    
    root.mainloop()