import tkinter as tk
from tkinter import ttk, messagebox
from backend.user_service import UserService

class UsersHomePage(tk.Frame):
    """Staff user management home page."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="User Management", font=("Arial", 22)).pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add New User",
            width=20,
            command=self.open_add_user
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Edit User",
            width=20,
            command=self.open_edit_user
        ).grid(row=0, column=1, padx=5)

        self.table = ttk.Treeview(
            self,
            columns=("id", "name", "role", "location", "status"),
            show="headings"
        )

        for col, text in [
            ("id", "ID"),
            ("name", "Name"),
            ("role", "Role"),
            ("location", "Location"),
            ("status", "Status"),
        ]:
            self.table.heading(col, text=text)

        self.table.column("id", width=0, stretch=False)

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_users()

    def load_users(self):
        for row in self.table.get_children():
            self.table.delete(row)

        users = UserService.get_all_users()

        for u in users:
            name = f"{u.first_name} {u.last_name}"
            status = "Active" if u.is_active else "Inactive"
            location = u.location.name if u.location else "N/A"

            self.table.insert(
                "",
                "end",
                values=(u.user_id, name, u.role, location, status)
            )

    def open_add_user(self):
        from ui.user_management.add_user_page import AddUserPage
        self.main_window.load_page(AddUserPage)

    def open_edit_user(self):
        from ui.user_management.edit_user_page import EditUserPage
        self.main_window.load_page(EditUserPage)