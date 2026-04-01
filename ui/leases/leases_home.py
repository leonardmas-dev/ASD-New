# Student: Thierno Batiga     StudentID: 24024769

import tkinter as tk
from tkinter import ttk, messagebox
from database.session import get_session
from database.models import Lease, Tenant, Apartment, Location

class LeasesHome(tk.Frame):
    """Staff overview of all leases."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Leases", font=("Arial", 22)).pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Edit Lease",
            width=18,
            command=self.open_edit_page
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="End Lease",
            width=18,
            command=self.end_lease
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="Refresh",
            width=12,
            command=self.refresh_table
        ).grid(row=0, column=2, padx=5)

        self.table = ttk.Treeview(
            self,
            columns=("id", "tenant", "apartment", "rent", "start", "end", "active"),
            show="headings",
        )

        for col, text in [
            ("id", "ID"),
            ("tenant", "Tenant"),
            ("apartment", "Apartment"),
            ("rent", "Monthly Rent"),
            ("start", "Start Date"),
            ("end", "End Date"),
            ("active", "Active"),
        ]:
            self.table.heading(col, text=text)

        self.table.column("id", width=0, stretch=False)
        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

    def load_data(self):
        db = get_session()
        rows = (
            db.query(Lease, Tenant, Apartment, Location)
            .join(Tenant, Lease.tenant_id == Tenant.tenant_id)
            .join(Apartment, Lease.apartment_id == Apartment.apartment_id)
            .join(Location, Apartment.location_id == Location.location_id)
            .filter(Lease.is_active == True)
            .all()
        )
        db.close()

        for lease, tenant, apt, loc in rows:
            apt_label = f"{loc.city} - Apt {apt.apartment_id}"
            self.table.insert(
                "",
                "end",
                values=(
                    lease.lease_id,
                    f"{tenant.first_name} {tenant.last_name}",
                    apt_label,
                    f"£{lease.monthly_rent}",
                    lease.start_date.strftime("%Y-%m-%d"),
                    lease.end_date.strftime("%Y-%m-%d"),
                    "Yes" if lease.is_active else "No",
                ),
            )

    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self.load_data()

    def _get_selected_lease_id(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Error", "Select a lease first.")
            return None
        values = self.table.item(selected[0], "values")
        return int(values[0])

    def end_lease(self):
        lease_id = self._get_selected_lease_id()
        if lease_id is None:
            return

        db = get_session()
        lease = db.query(Lease).filter(Lease.lease_id == lease_id).first()

        if not lease:
            db.close()
            messagebox.showerror("Error", "Lease not found.")
            return

        apt = db.query(Apartment).filter(Apartment.apartment_id == lease.apartment_id).first()

        lease.is_active = False
        if apt:
            apt.is_available = True

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Lease ended.")
        self.refresh_table()

    def open_edit_page(self):
        from ui.leases.edit_lease_page import EditLeasePage
        self.main_window.load_page(EditLeasePage)