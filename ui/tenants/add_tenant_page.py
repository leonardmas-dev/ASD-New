import tkinter as tk
from tkinter import ttk, messagebox

from backend.tenant_service import TenantService
from database.session import get_session
from database.models import Location


class AddTenantPage(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Add New Tenant", font=("Arial", 18, "bold")).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=10)

        self.first_name = self._add_field(form, "First Name")
        self.last_name = self._add_field(form, "Last Name")
        self.email = self._add_field(form, "Email")
        self.phone = self._add_field(form, "Phone")
        self.ni_number = self._add_field(form, "NI Number")
        self.occupation = self._add_field(form, "Occupation")

        self.username = self._add_field(form, "Tenant Username")
        self.password = self._add_field(form, "Tenant Password", show="*")

        tk.Label(form, text="Location").grid(row=form.grid_size()[1], column=0, sticky="w")
        self.location_box = ttk.Combobox(form)
        self.location_box.grid(row=form.grid_size()[1] - 1, column=1, pady=5)

        self.load_locations()

        tk.Button(self, text="Create Tenant", command=self.save_tenant, width=20).pack(pady=10)
        from ui.tenants.tenants_home import TenantsHome
        tk.Button(self, text="Back", command=lambda: main_window.load_page(TenantsHome)).pack()

    def _add_field(self, parent, label, show=None):
        row_index = parent.grid_size()[1]
        tk.Label(parent, text=label).grid(row=row_index, column=0, sticky="w")
        entry = tk.Entry(parent, show=show)
        entry.grid(row=row_index, column=1, pady=5)
        return entry

    def load_locations(self):
        db = get_session()
        locations = db.query(Location).all()
        db.close()
        self.location_box["values"] = [f"{loc.location_id} - {loc.city}" for loc in locations]

    def save_tenant(self):
        if TenantService.ni_number_exists(self.ni_number.get()):
            messagebox.showerror("Error", "An account with this National Insurance number already exists.")
            return

        if not self.username.get().strip() or not self.password.get().strip():
            messagebox.showerror("Error", "Tenant username and password are required.")
            return

        if TenantService.tenant_username_exists(self.username.get().strip()):
            messagebox.showerror("Error", "This tenant username is already in use.")
            return

        if not self.location_box.get():
            messagebox.showerror("Error", "Please select a location.")
            return

        loc_id = int(self.location_box.get().split(" - ")[0])

        data = {
            "first_name": self.first_name.get().strip(),
            "last_name": self.last_name.get().strip(),
            "email": self.email.get().strip(),
            "phone": self.phone.get().strip(),
            "ni_number": self.ni_number.get().strip(),
            "occupation": self.occupation.get().strip(),
            "location_id": loc_id,
            "username": self.username.get().strip(),
            "password": self.password.get().strip(),
        }

        TenantService.create_tenant(data)
        messagebox.showinfo("Success", "Tenant and tenant portal account created.")

        from ui.tenants.tenant_list_page import TenantList
        self.main_window.load_page(TenantList)