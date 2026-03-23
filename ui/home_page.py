import tkinter as tk

class HomePage(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.session = main_window.user_session

        label = tk.Label(self, text="Welcome to Paragon Apartments System", font=("Arial", 24))
        label.pack(pady=50)