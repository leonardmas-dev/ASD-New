import tkinter as tk
from tkinter import ttk

from database.session import get_session
from database.models import Tenant


class TenantListPage(tk.Frame):
    """List of tenants for selection."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Select Tenant", font=("Arial", 22)).pack(pady=20)

        self.table = ttk.Treeview(
            self,
            columns=("id", "name", "email", "active"),
            show="headings",
        )

        for col, text in [
            ("id", "ID"),
            ("name", "Name"),
            ("email", "Email"),
            ("active", "Active"),
        ]:
            self.table.heading(col, text=text)

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

    def load_data(self):
        db = get_session()
        tenants = db.query(Tenant).all()
        db.close()

        for t in tenants:
            self.table.insert(
                "",
                "end",
                values=(
                    t.tenant_id,
                    f"{t.first_name} {t.last_name}",
                    t.email,
                    "Yes" if t.is_active else "No",
                ),
            )