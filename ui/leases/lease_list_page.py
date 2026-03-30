import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database.session import SessionLocal
from backend.lease_service import LeaseService


class LeaseListPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Active Lease Agreements", font=("Arial", 18, "bold")).pack(pady=10)

        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=20, pady=5)

        tk.Label(search_frame, text="Search by Lease ID:").pack(side="left")
        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side="left", padx=5)

        tk.Button(search_frame, text="Find Lease", command=self.filter_leases).pack(side="left")

        tree_frame = tk.Frame(self)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

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

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Refresh Leases", command=self.load_leases, width=15).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Edit / Terminate",
            bg="#3498db",
            fg="white",
            width=18,
            command=self.go_to_edit,
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Quick Termination",
            bg="#e67e22",
            fg="white",
            width=18,
            command=self.process_termination,
        ).pack(side="left", padx=10)

        from ui.leases.leases_home import LeasesHome
        tk.Button(
            btn_frame,
            text="Back",
            bg="#95a5a6",
            fg="white",
            width=12,
            command=lambda: self.controller.load_page(LeasesHome),
        ).pack(side="left", padx=10)

        self.load_leases()

    def load_leases(self):
        # reload table from db
        for item in self.tree.get_children():
            self.tree.delete(item)

        db = SessionLocal()
        service = LeaseService(db)
        try:
            leases = service.get_all_leases()
        finally:
            db.close()

        for l in leases:
            tenant_name = f"{l['first_name']} {l['last_name']}"
            self.tree.insert(
                "",
                "end",
                values=(
                    l['lease_id'],
                    tenant_name,
                    l['apartment_id'],
                    l['start_date'],
                    l['end_date'],
                    f"£{l['monthly_rent']}",
                ),
            )

    def go_to_edit(self):
        # open edit page with selected lease
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Selection", "Please select a lease to manage.")
            return

        l_data = self.tree.item(selected)['values']

        from ui.leases.edit_lease_page import EditLeasePage
        if self.controller:
            self.controller.load_page(
                EditLeasePage,
                lease_id=l_data[0],
                tenant_name=l_data[1],
                apt_id=l_data[2],
                rent=l_data[5],
            )

    def process_termination(self):
        # quick termination from list
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Selection", "Please select a lease.")
            return

        values = self.tree.item(selected)['values']
        lease_id = values[0]
        apt_id = values[2]

        confirm = messagebox.askyesno("Confirm", f"Are you sure you want to terminate Lease #{lease_id}?")
        if not confirm:
            return

        db = SessionLocal()
        service = LeaseService(db)
        try:
            penalty = service.terminate_lease(lease_id, apt_id)
        finally:
            db.close()

        if penalty is not None:
            messagebox.showinfo("Success", f"Lease Terminated.\nPenalty: £{penalty:.2f}")
            self.load_leases()
        else:
            messagebox.showerror("Error", "Could not process termination.")

    def filter_leases(self):
        query = self.search_entry.get().lower()
        if not query:
            self.load_leases()
            return
        for item in self.tree.get_children():
            if query not in str(self.tree.item(item)['values'][0]).lower():
                self.tree.detach(item)