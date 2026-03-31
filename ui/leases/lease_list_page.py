import tkinter as tk
from tkinter import ttk

from database.session import get_session
from database.models import Lease, Tenant, Apartment


class LeaseListPage(tk.Frame):
    """List of leases for selection."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Select Lease", font=("Arial", 22)).pack(pady=20)

        self.table = ttk.Treeview(
            self,
            columns=("id", "tenant", "apartment", "active"),
            show="headings",
        )

        for col, text in [
            ("id", "Lease ID"),
            ("tenant", "Tenant"),
            ("apartment", "Apartment"),
            ("active", "Active"),
        ]:
            self.table.heading(col, text=text)

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

    def load_data(self):
        db = get_session()
        rows = (
            db.query(Lease, Tenant, Apartment)
            .join(Tenant, Lease.tenant_id == Tenant.tenant_id)
            .join(Apartment, Lease.apartment_id == Apartment.apartment_id)
            .all()
        )
        db.close()

        for lease, tenant, apt in rows:
            loc = apt.location
            apt_label = f"{loc.city} - Apt {apt.apartment_id}"

            self.table.insert(
                "",
                "end",
                values=(
                    lease.lease_id,
                    f"{tenant.first_name} {tenant.last_name}",
                    apt_label,
                    "Yes" if lease.is_active else "No",
                ),
            )