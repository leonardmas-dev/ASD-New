import tkinter as tk
from tkinter import ttk, messagebox
from backend.user_service import UserService
from database.session import get_session
from database.models import Location

class AddUserPage(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Add New User", font=("Arial", 18, "bold")).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=10)

        # form fields
        self.first_name = self._add_field(form, "First Name")
        self.last_name = self._add_field(form, "Last Name")
        self.email = self._add_field(form, "Email")
        self.phone = self._add_field(form, "Phone")
        self.username = self._add_field(form, "Username")
        self.password = self._add_field(form, "Password", show="*")

        tk.Label(form, text="Role").grid(row=6, column=0, sticky="w")
        self.role_box = ttk.Combobox(form, values=["FrontDesk", "FinanceManager", "MaintenanceStaff", "Manager"])
        self.role_box.grid(row=6, column=1, pady=5)

        tk.Label(form, text="Location").grid(row=7, column=0, sticky="w")
        self.location_box = ttk.Combobox(form)
        self.location_box.grid(row=7, column=1, pady=5)

        self.load_locations()

        tk.Button(self, text="Create User", command=self.save_user, width=20).pack(pady=10)
        from ui.user_management.users_home import UsersHomePage
        tk.Button(self, text="Back", command=lambda: main_window.load_page(UsersHomePage)).pack()

    # helper to create a labeled entry
    def _add_field(self, parent, label, show=None):
        tk.Label(parent, text=label).grid(sticky="w")
        entry = tk.Entry(parent, show=show)
        entry.grid(row=parent.grid_size()[1]-1, column=1, pady=5)
        return entry

    # load locations into dropdown
    def load_locations(self):
        db = get_session()
        locations = db.query(Location).all()
        db.close()
        self.location_box["values"] = [f"{loc.location_id} - {loc.city}" for loc in locations]

    # save new user
    def save_user(self):
        if UserService.username_exists(self.username.get()):
            messagebox.showerror("Error", "Username already exists.")
            return

        loc_id = int(self.location_box.get().split(" - ")[0])

        data = {
            "first_name": self.first_name.get(),
            "last_name": self.last_name.get(),
            "email": self.email.get(),
            "phone": self.phone.get(),
            "username": self.username.get(),
            "password": self.password.get(),
            "role": self.role_box.get(),
            "location_id": loc_id
        }

        UserService.create_user(data)
        messagebox.showinfo("Success", "User created.")
        from ui.user_management.users_home import UsersHomePage
        self.main_window.load_page(UsersHomePage)