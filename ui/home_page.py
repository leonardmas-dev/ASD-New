import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, user_session=None):
        super().__init__(parent)

        # Basic welcome label for now
        label = tk.Label(self, text="Welcome to PAMS", font=("Arial", 24))
        label.pack(pady=50) 