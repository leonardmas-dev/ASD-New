import tkinter as tk

class MaintenanceHome(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Maintenance", font=("Arial", 18)).pack(pady=40)