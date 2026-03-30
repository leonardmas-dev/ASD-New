import tkinter as tk
from ui.tenants.add_tenant_page import AddTenantPage
from ui.tenants.tenant_list_page import TenantList
from ui.tenants.edit_tenant_page import EditTenantPage


class TenantsHome(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Tenant Management", font=("Arial", 18, "bold")).pack(pady=20)

        tk.Button(
            self,
            text="Add Tenant",
            width=25,
            command=lambda: main_window.load_page(AddTenantPage)
        ).pack(pady=10)

        tk.Button(
            self,
            text="View Tenants",
            width=25,
            command=lambda: main_window.load_page(TenantList)
        ).pack(pady=10)

        tk.Button(
            self,
            text="Edit Tenants",
            width=25,
            command=lambda: main_window.load_page(EditTenantPage)
        ).pack(pady=10)

        tk.Button(
            self,
            text="Back",
            width=25,
            command=main_window.go_home
        ).pack(pady=20)