import tkinter as tk
from tkinter import ttk
from backend.tenant_service import fetch_tenants


class TenantList(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Tenant Information", font=("Arial", 16, "bold")).pack(pady=10)

        columns = ("Tenant ID", "First Name", "Last Name", "Phone", "Email", "Location")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        self.tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_data()

        tk.Button(self, text="Go Home", command=self.go_home).pack(pady=10)

    def load_data(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Insert fresh data
        for tenant in fetch_tenants():
            self.tree.insert(
                "",
                "end",
                values=(
                    tenant.tenant_id,
                    tenant.first_name,
                    tenant.last_name,
                    tenant.phone,
                    tenant.email,
                    tenant.location.city if tenant.location else "N/A"
                )
            )

    def go_home(self):
        from ui.tenants.tenants_home import TenantsHome
        self.main_window.load_page(TenantsHome)