# Student: Leonard Masters     StudentID: 24031618

import tkinter as tk
from tkinter import ttk

from database.session import get_session
from database.models import Tenant


class TenantListPage(tk.Frame):
    """List of tenants for selection."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Tenant List", font=("Arial", 22)).pack(pady=20)

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
        self.table.column("id", width=0, stretch=False)

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

        # back button
        tk.Button(self, text="Back", width=18, command=self.go_back).pack(pady=10)

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

    def go_back(self):
        from ui.tenants.tenants_home import TenantsHome
        self.main_window.load_page(TenantsHome)