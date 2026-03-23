import tkinter as tk
from tkinter import ttk

class MainWindow(tk.Tk):
    def __init__(self, user_session=None):
        super().__init__()

        # Basic window setup
        self.title("PAMS - Paragon Apartment Management System")
        self.geometry("1200x700")

        # Store logged-in user info (used later for role-based menus)
        self.user_session = user_session

        # Left navigation panel
        self.nav_frame = tk.Frame(self, width=250, bg="#2c3e50")
        self.nav_frame.pack(side="left", fill="y")

        # Main content area where pages will load
        self.content_frame = tk.Frame(self, bg="#ecf0f1")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Load navigation menu
        from ui.navigation import Navigation
        Navigation(self.nav_frame, self)

    def load_page(self, page_class):
        # Clear whatever page is currently displayed
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Create and display the new page
        page = page_class(self.content_frame, self)
        page.pack(fill="both", expand=True)


def start_ui(user_session=None):
    # Launch the main window (used by app.py)
    app = MainWindow(user_session)
    app.mainloop()