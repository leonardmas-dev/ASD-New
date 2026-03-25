import tkinter as tk

class TenantDashboard(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        tk.Label(self, text="Tenant Dashboard", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self, text="Welcome to your tenant portal.").pack(pady=10)