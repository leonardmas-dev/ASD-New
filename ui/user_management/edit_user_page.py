import tkinter as tk
from tkinter import ttk, messagebox
from backend.user_service import UserService
from database.session import get_session
from database.models import Location

class EditUserPage(tk.Frame):
    def __init__(self, parent, main_window, user_id):
        super().__init__(parent)
        self.main_window = main_window
        self.user_id = user_id

        tk.Label(self, text="Edit User", font=("Arial", 18, "bold")).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=10)

        self.first_name = self._add_field(form, "First Name")
        self.last_name = self._add_field(form, "Last Name")
        self.email = self._add_field(form, "Email")
        self.phone = self._add_field(form, "Phone")
        self.password = self._add_field(form, "New Password (optional)", show="*")

        tk.Label(form, text="Role").grid(row=5, column=0, sticky="w")
        self.role_box = ttk.Combobox(form, values=["FrontDesk", "FinanceManager", "MaintenanceStaff", "Manager"])
        self.role_box.grid(row=5, column=1, pady=5)

        tk.Label(form, text="Location").grid(row=6, column=0, sticky="w")
        self.location_box = ttk.Combobox(form)
        self.location_box.grid(row=6, column=1, pady=5)

        tk.Label(form, text="Active").grid(row=7, column=0, sticky="w")
        self.active_var = tk.BooleanVar()
        tk.Checkbutton(form, variable=self.active_var).grid(row=7, column=1)

        self.load_locations()
        self.load_user()

        tk.Button(self, text="Save Changes", command=self.save_user, width=20).pack(pady=10)
        tk.Button(self, text="Back", command=lambda: main_window.load_page("users_home")).pack()

    def _add_field(self, parent, label, show=None):
        tk.Label(parent, text=label).grid(sticky="w")
        entry = tk.Entry(parent, show=show)
        entry.grid(row=parent.grid_size()[1]-1, column=1, pady=5)
        return entry

    def load_locations(self):
        db = get_session()
        locations = db.query(Location).all()
        db.close()
        self.location_box["values"] = [f"{loc.location_id} - {loc.city}" for loc in locations]

    def load_user(self):
        user = UserService.get_user_by_id(self.user_id)

        self.first_name.insert(0, user.first_name)
        self.last_name.insert(0, user.last_name)
        self.email.insert(0, user.email)
        self.phone.insert(0, user.phone)
        self.role_box.set(user.role)
        self.location_box.set(f"{user.location_id} - {user.location.city}")
        self.active_var.set(user.is_active)

    def save_user(self):
        loc_id = int(self.location_box.get().split(" - ")[0])

        data = {
            "first_name": self.first_name.get(),
            "last_name": self.last_name.get(),
            "email": self.email.get(),
            "phone": self.phone.get(),
            "role": self.role_box.get(),
            "location_id": loc_id,
            "password": self.password.get() if self.password.get() else None
        }

        UserService.update_user(self.user_id, data)

        # update active flag
        if not self.active_var.get():
            UserService.deactivate_user(self.user_id)

        messagebox.showinfo("Success", "User updated.")
        self.main_window.load_page("users_home")