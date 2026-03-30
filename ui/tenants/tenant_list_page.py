import tkinter as tk
from tkinter import ttk
from backend.tenant_service import fetch_tenants


class TenantList(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tenant_list_title = tk.Label(self, text="Tenant Information")
        tenant_list_title.pack()

        columns = ("Tenant ID", "First Name", "Last Name", "Phone", "Email", "Apartment")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_data()

        go_homebtn = tk.Button(self, text="Go Home", command=self.go_home)
        go_homebtn.pack(pady=10)

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

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
                    tenant.location_id
                )
            )

    def go_home(self):
        from ui.tenants.tenants_home import TenantsHome
        self.main_window.load_page(TenantsHome)