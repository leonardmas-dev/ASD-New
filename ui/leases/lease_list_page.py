import tkinter as tk
from tkinter import ttk

from database.session import get_session
from database.models import Lease, Tenant, Apartment


class LeaseListPage(tk.Frame):
    """Read-only list of leases."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Lease List", font=("Arial", 22)).pack(pady=20)

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

        tk.Button(self, text="Back", width=10, command=self.go_back).pack(pady=15)

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

    def go_back(self):
        from ui.leases.leases_home import LeasesHome
        self.main_window.load_page(LeasesHome)