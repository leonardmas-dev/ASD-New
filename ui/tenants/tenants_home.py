# This page is for admin/manager and landlord not tenants portal.

import tkinter as tk


class TenantsHome(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Tenants Home Page", font=("Arial", 18)).pack(pady=40)
        

        
        tk.Button(self, text="View Tenants", command=self.open_tenant_list).pack(pady=20)

    def open_tenant_list(self):
        #loading tenant page like this leads to not having circular imports
        from ui.tenants.tenant_list_page import TenantList
        self.main_window.load_page(TenantList)