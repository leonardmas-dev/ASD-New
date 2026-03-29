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

        # form fields
        self.first_name = self._add_field(form, "First Name")
        self.last_name = self._add_field(form, "Last Name")
        self.email = self._add_field(form, "Email")
        

        self.phone = self._add_field(form, "Phone")

        self.ni_number = self._add_field(form, "NI Number")
        self.occupation = self._add_field(form, "Occupation")

        tk.Label(form, text="Location").grid(row=7, column=0, sticky="w")
        self.location_box = ttk.Combobox(form)
        self.location_box.grid(row=7, column=1, pady=5)

        self.load_locations()

        tk.Button(self, text="Create Tenant", command=self.save_tenant, width=20).pack(pady=10)
        from ui.tenants.tenants_home import TenantsHome
        tk.Button(self, text="Back", command=lambda: main_window.load_page(TenantsHome)).pack()

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
    def save_tenant(self):
        if TenantService.ni_number_exists(self.ni_number.get()):
            messagebox.showerror("Error", "An Account with this National Insurance number already exists.")
            return

        loc_id = int(self.location_box.get().split(" - ")[0])

        data = {
            "first_name": self.first_name.get(),
            "last_name": self.last_name.get(),
            "email": self.email.get(),

            "phone": self.phone.get(),
            "ni_number": self.ni_number.get(),
            "occupation": self.occupation.get(),
            
            "location_id": loc_id
        }

        TenantService.create_tenant(data)
        messagebox.showinfo("Success", "Tenant Added.")
        from ui.tenants.tenant_list_page import TenantList
        self.main_window.load_page(TenantList)