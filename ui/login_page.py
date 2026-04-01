# Student: Yaseen Sassi     StudentID: 24023127

import tkinter as tk
from tkinter import messagebox

from database.session import get_session
from backend.auth_service import AuthService
from ui.main_window import MainWindow


class LoginPage(tk.Tk):
    """Login window for Paragon Apartments."""

    def __init__(self):
        super().__init__()
        self.title("Paragon Apartments Login")
        self.geometry("900x700")

        tk.Label(self, text="Username").pack(pady=(30, 5))
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Password").pack(pady=(15, 5))
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Login", command=self.handle_login).pack(pady=25)

    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both fields")
            return

        db = get_session()
        auth = AuthService(db)

        try:
            user_session = auth.authenticate(username, password)
        finally:
            db.close()

        if user_session is None:
            messagebox.showerror("Login Failed", "Invalid username or password")
            return

        # Close login window and open main application window
        self.destroy()
        app = MainWindow(user_session=user_session)
        app.mainloop()