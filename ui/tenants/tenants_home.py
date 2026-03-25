import tkinter as tk
from tenants.tenant_list_page import TenantList

class TenantsHome(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Tenants Home Page", font=("Arial", 18)).pack(pady=40)
        

        
        tk.Button(self, text="View Tenants", command=lambda: main_window.load_page(TenantList)).pack(pady=20)