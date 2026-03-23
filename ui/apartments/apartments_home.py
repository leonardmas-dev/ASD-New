import tkinter as tk

class ApartmentsHome(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Apartments", font=("Arial", 18)).pack(pady=40)