import tkinter as tk

class ComplaintsHome(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Complaints", font=("Arial", 18)).pack(pady=40)