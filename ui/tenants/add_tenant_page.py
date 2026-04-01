# Student: Leonard Masters     StudentID: 24031618

import tkinter as tk
from tkinter import ttk, messagebox
import re

from database.session import get_session
from database.models import Tenant, TenantAccount, Location
from passlib.hash import bcrypt


class AddTenantPage(tk.Frame):
    """Create tenant + linked tenant account with full validation."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Add Tenant", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        # location dropdown
        tk.Label(form, text="Location:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.location_var = tk.StringVar()
        self.location_cb = ttk.Combobox(form, textvariable=self.location_var, state="readonly", width=30)
        self.location_cb.grid(row=0, column=1, padx=5, pady=3)

        labels = [
            "NI Number", "First Name", "Last Name",
            "Phone", "Email", "Occupation",
            "References", "Apartment Requirements",
            "Tenant Username", "Tenant Password",
        ]
        self.entries = {}

        for i, label in enumerate(labels, start=1):
            tk.Label(form, text=f"{label}:").grid(row=i, column=0, sticky="e", padx=5, pady=3)
            show = "*" if "Password" in label else None
            e = tk.Entry(form, width=32, show=show)
            e.grid(row=i, column=1, padx=5, pady=3)
            self.entries[label] = e

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Save Tenant", width=18, command=self.save_tenant).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", width=18, command=self.go_back).grid(row=0, column=1, padx=5)

        self.load_locations()

    # load locations
    def load_locations(self):
        db = get_session()
        locations = db.query(Location).filter(Location.is_active == True).all()
        db.close()

        data = [(str(loc.location_id), f"{loc.name} - {loc.city}") for loc in locations]
        self.location_cb["values"] = [label for _, label in data]
        self._location_map = {label: loc_id for loc_id, label in data}

        if data:
            self.location_cb.current(0)

    # validation helpers
    def validate_email(self, email):
        return "@" in email and "." in email and len(email) <= 255

    def validate_phone(self, phone):
        return bool(re.fullmatch(r"[0-9 +]{5,50}", phone))

    def validate_name(self, name):
        return bool(re.fullmatch(r"[A-Za-z \-]{1,255}", name))

    def validate_username(self, username):
        return bool(re.fullmatch(r"[A-Za-z0-9_]{3,50}", username))

    def validate_ni(self, ni):
        return bool(re.fullmatch(r"[A-Za-z0-9]{2,50}", ni))

    # save tenant
    def save_tenant(self):
        loc_label = self.location_var.get()
        if not loc_label:
            messagebox.showerror("Error", "Location is required.")
            return

        # extract fields
        ni = self.entries["NI Number"].get().strip()
        first = self.entries["First Name"].get().strip()
        last = self.entries["Last Name"].get().strip()
        phone = self.entries["Phone"].get().strip()
        email = self.entries["Email"].get().strip()
        occupation = self.entries["Occupation"].get().strip()
        refs = self.entries["References"].get().strip()
        reqs = self.entries["Apartment Requirements"].get().strip()
        username = self.entries["Tenant Username"].get().strip()
        password = self.entries["Tenant Password"].get().strip()

        # required fields
        if not all([ni, first, last, phone, email, username, password]):
            messagebox.showerror("Error", "All required fields must be filled.")
            return

        # field validation
        if not self.validate_ni(ni):
            messagebox.showerror("Error", "Invalid NI Number.")
            return

        if not self.validate_name(first):
            messagebox.showerror("Error", "Invalid first name.")
            return

        if not self.validate_name(last):
            messagebox.showerror("Error", "Invalid last name.")
            return

        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number.")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email address.")
            return

        if not self.validate_username(username):
            messagebox.showerror("Error", "Invalid username. Use letters, numbers, underscore (3–50 chars).")
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters.")
            return

        if len(password) > 72:
            messagebox.showerror("Error", "Password cannot exceed 72 characters.")
            return

        db = get_session()

        # unique username check
        existing = db.query(TenantAccount).filter(TenantAccount.username == username).first()
        if existing:
            db.close()
            messagebox.showerror("Error", "Username already exists.")
            return

        location_id = int(self._location_map[loc_label])

        # create tenant
        tenant = Tenant(
            location_id=location_id,
            ni_number=ni,
            first_name=first,
            last_name=last,
            phone=phone,
            email=email,
            occupation=occupation or None,
            references_text=refs or None,
            apartment_requirements=reqs or None,
        )
        db.add(tenant)
        db.flush()

        # create tenant account
        account = TenantAccount(
            tenant_id=tenant.tenant_id,
            username=username,
            password_hash=bcrypt.hash(password[:72]),
            is_active=True,
        )
        db.add(account)

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Tenant created successfully.")
        self.go_back()

    def go_back(self):
        from ui.tenants.tenants_home import TenantsHome
        self.main_window.load_page(TenantsHome)