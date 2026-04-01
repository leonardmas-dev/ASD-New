import tkinter as tk
from tkinter import ttk, messagebox
import re

from database.session import get_session
from database.models import Tenant, TenantAccount, Location
from passlib.hash import bcrypt


class EditTenantPage(tk.Frame):
    """Edit tenant + linked tenant account with full validation."""

    def __init__(self, parent, main_window, tenant_id):
        super().__init__(parent)
        self.main_window = main_window
        self.tenant_id = tenant_id

        tk.Label(self, text="Edit Tenant", font=("Arial", 22)).pack(pady=20)

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
            "Tenant Username", "New Password (optional)",
        ]
        self.entries = {}

        for i, label in enumerate(labels, start=1):
            tk.Label(form, text=f"{label}:").grid(row=i, column=0, sticky="e", padx=5, pady=3)
            show = "*" if "Password" in label else None
            e = tk.Entry(form, width=32, show=show)
            e.grid(row=i, column=1, padx=5, pady=3)
            self.entries[label] = e

        # active checkbox
        self.active_var = tk.BooleanVar()
        tk.Checkbutton(form, text="Active", variable=self.active_var).grid(
            row=len(labels)+1, column=1, sticky="w", pady=5
        )

        # buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Save Changes", width=18, command=self.save_changes).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", width=18, command=self.go_back).grid(row=0, column=1, padx=5)

        self.load_locations()
        self.load_tenant()

    # load locations
    def load_locations(self):
        db = get_session()
        locations = db.query(Location).filter(Location.is_active == True).all()
        db.close()

        data = [(str(loc.location_id), f"{loc.name} - {loc.city}") for loc in locations]
        self.location_cb["values"] = [label for _, label in data]
        self._location_map = {label: loc_id for loc_id, label in data}

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

    # load tenant + account
    def load_tenant(self):
        db = get_session()
        tenant = db.query(Tenant).filter(Tenant.tenant_id == self.tenant_id).first()

        if not tenant:
            db.close()
            messagebox.showerror("Error", "Tenant not found.")
            self.go_back()
            return

        account = tenant.tenant_account

        # set location
        for label, loc_id in self._location_map.items():
            if loc_id == tenant.location_id:
                self.location_var.set(label)
                break

        # fill fields
        self.entries["NI Number"].insert(0, tenant.ni_number)
        self.entries["First Name"].insert(0, tenant.first_name)
        self.entries["Last Name"].insert(0, tenant.last_name)
        self.entries["Phone"].insert(0, tenant.phone)
        self.entries["Email"].insert(0, tenant.email)
        self.entries["Occupation"].insert(0, tenant.occupation or "")
        self.entries["References"].insert(0, tenant.references_text or "")
        self.entries["Apartment Requirements"].insert(0, tenant.apartment_requirements or "")

        if account:
            self.entries["Tenant Username"].insert(0, account.username)

        self.active_var.set(tenant.is_active and (account.is_active if account else True))

        db.close()

    # save changes
    def save_changes(self):
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
        new_password = self.entries["New Password (optional)"].get().strip()
        is_active = self.active_var.get()

        # required fields
        if not all([ni, first, last, phone, email, username]):
            messagebox.showerror("Error", "All required fields must be filled.")
            return

        # validation
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

        if new_password:
            if len(new_password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters.")
                return
            if len(new_password) > 72:
                messagebox.showerror("Error", "Password cannot exceed 72 characters.")
                return

        db = get_session()
        tenant = db.query(Tenant).filter(Tenant.tenant_id == self.tenant_id).first()

        if not tenant:
            db.close()
            messagebox.showerror("Error", "Tenant not found.")
            self.go_back()
            return

        account = tenant.tenant_account

        # unique username check
        existing = (
            db.query(TenantAccount)
            .filter(TenantAccount.username == username, TenantAccount.tenant_id != self.tenant_id)
            .first()
        )
        if existing:
            db.close()
            messagebox.showerror("Error", "Username already exists.")
            return

        location_id = int(self._location_map[loc_label])

        # update tenant
        tenant.location_id = location_id
        tenant.ni_number = ni
        tenant.first_name = first
        tenant.last_name = last
        tenant.phone = phone
        tenant.email = email
        tenant.occupation = occupation or None
        tenant.references_text = refs or None
        tenant.apartment_requirements = reqs or None
        tenant.is_active = is_active

        # update or create account
        if account is None:
            if not new_password:
                db.close()
                messagebox.showerror("Error", "Password required to create tenant account.")
                return

            account = TenantAccount(
                tenant_id=tenant.tenant_id,
                username=username,
                password_hash=bcrypt.hash(new_password[:72]),
                is_active=is_active,
            )
            db.add(account)

        else:
            account.username = username
            if new_password:
                account.password_hash = bcrypt.hash(new_password[:72])
            account.is_active = is_active

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Tenant updated successfully.")
        self.go_back()

    def go_back(self):
        from ui.tenants.tenants_home import TenantsHome
        self.main_window.load_page(TenantsHome)