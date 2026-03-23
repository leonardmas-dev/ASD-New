import tkinter as tk

class TenantsHome(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Tenants", font=("Arial", 18)).pack(pady=40)