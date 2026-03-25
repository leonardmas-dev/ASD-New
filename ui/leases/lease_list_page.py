import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Path fix for backend imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.lease_service import get_all_leases, terminate_lease

class LeaseListPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Active Lease Agreements", font=("Arial", 18, "bold")).pack(pady=10)

        # --- Search Section ---
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=20, pady=5)
        
        tk.Label(search_frame, text="Search by Lease ID:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)
        
        tk.Button(search_frame, text="Find Lease", command=self.filter_leases).pack(side="left")

        # --- Table Section ---
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Columns match your MySQL: lease_id, tenant (name), apartment, start, end, rent
        columns = ("id", "tenant", "apartment", "start", "end", "rent")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("tenant", text="Tenant Name")
        self.tree.heading("apartment", text="Apt ID")
        self.tree.heading("start", text="Start Date")
        self.tree.heading("end", text="End Date")
        self.tree.heading("rent", text="Monthly Rent")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # --- Bottom Buttons ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Refresh Leases", command=self.load_leases, width=15).pack(side="left", padx=10)
        
        # This button now triggers the 5% penalty logic
        tk.Button(btn_frame, text="Early Termination", 
                  bg="#e67e22", fg="white", width=20, 
                  command=self.process_termination).pack(side="left", padx=10)

        # Initial data load
        self.load_leases()

    def load_leases(self):
        """Fetches real data from backend/lease_service.py"""
        for item in self.tree.get_children():
            self.tree.delete(item)

        leases = get_all_leases() # Real backend call
        for l in leases:
            # We show the tenant name (joined from tenant table in backend)
            tenant_name = f"{l['first_name']} {l['last_name']}"
            
            self.tree.insert("", "end", values=(
                l['lease_id'],
                tenant_name,
                l['apartment_id'],
                l['start_date'],
                l['end_date'],
                f"£{l['monthly_rent']}"
            ))

    def process_termination(self):
        """Processes early termination with the 5% penalty"""
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Selection", "Please select a lease to terminate.")
            return

        values = self.tree.item(selected)['values']
        lease_id = values[0]
        apt_id = values[2]

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to terminate Lease #{lease_id}?\nThis will apply a 5% penalty.")
        
        if confirm:
            penalty = terminate_lease(lease_id, apt_id) # Real backend call
            if penalty is not None:
                messagebox.showinfo("Success", f"Lease Terminated.\n\nEarly Termination Penalty: £{penalty:.2f}\nApartment {apt_id} is now Available.")
                self.load_leases() # Refresh the table
            else:
                messagebox.showerror("Error", "Could not process termination.")

    def filter_leases(self):
        # Local UI filtering logic
        query = self.search_entry.get().lower()
        if not query:
            self.load_leases()
            return
        for item in self.tree.get_children():
            if query not in str(self.tree.item(item)['values'][0]).lower():
                self.tree.detach(item)