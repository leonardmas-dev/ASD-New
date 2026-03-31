import tkinter as tk
from tkinter import ttk
from backend.user_service import UserService


class UsersHomePage(tk.Frame):
    """Staff user management home page."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="User Management", font=("Arial", 18, "bold")).pack(pady=10)

        # add user button
        tk.Button(
            self,
            text="Add New User",
            command=self.open_add_user,
            width=20
        ).pack(pady=5)

        # edit user button
        tk.Button(
            self,
            text="Edit User",
            command=self.open_edit_user_page,
            width=20
        ).pack(pady=5)

        # table of staff users
        self.table = ttk.Treeview(
            self,
            columns=("name", "role", "location", "status"),
            show="headings"
        )

        self.table.heading("name", text="Name")
        self.table.heading("role", text="Role")
        self.table.heading("location", text="Location")
        self.table.heading("status", text="Status")

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_users()

    # load all users into table
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
                values=(name, u.role, location, status)
            )

    # open add user page
    def open_add_user(self):
        from ui.user_management.add_user_page import AddUserPage
        self.main_window.load_page(AddUserPage)

    # open edit user page
    def open_edit_user_page(self):
        from ui.user_management.edit_user_page import EditUserPage
        self.main_window.load_page(EditUserPage)