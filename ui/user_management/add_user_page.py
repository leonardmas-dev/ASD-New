# Student: Yaseen Sassi     StudentID: 24023127

import tkinter as tk
from tkinter import ttk, messagebox
import re
from database.session import get_session
from database.models import User, Location
from passlib.hash import bcrypt

ROLES = ["FrontDesk", "FinanceManager", "MaintenanceStaff", "Manager"]

class AddUserPage(tk.Frame):
    """Create staff user account with full validation."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Add Staff User", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Location:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.location_var = tk.StringVar()
        self.location_cb = ttk.Combobox(form, textvariable=self.location_var, state="readonly", width=30)
        self.location_cb.grid(row=0, column=1, padx=5, pady=3)

        labels = [
            "First Name", "Last Name", "Email", "Phone",
            "Username", "Password",
        ]
        self.entries = {}

        for i, label in enumerate(labels, start=1):
            tk.Label(form, text=f"{label}:").grid(row=i, column=0, sticky="e", padx=5, pady=3)
            show = "*" if "Password" in label else None
            e = tk.Entry(form, width=32, show=show)
            e.grid(row=i, column=1, padx=5, pady=3)
            self.entries[label] = e

        tk.Label(form, text="Role:").grid(row=len(labels)+1, column=0, sticky="e", padx=5, pady=3)
        self.role_var = tk.StringVar()
        self.role_cb = ttk.Combobox(form, textvariable=self.role_var, state="readonly", values=ROLES, width=30)
        self.role_cb.grid(row=len(labels)+1, column=1, padx=5, pady=3)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Save User", width=18, command=self.save_user).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", width=18, command=self.go_back).grid(row=0, column=1, padx=5)

        self.load_locations()
        if ROLES:
            self.role_cb.current(0)

    def load_locations(self):
        db = get_session()
        locations = db.query(Location).filter(Location.is_active == True).all()
        db.close()

        data = [(str(loc.location_id), f"{loc.name} - {loc.city}") for loc in locations]
        self.location_cb["values"] = [label for _, label in data]
        self._location_map = {label: loc_id for loc_id, label in data}

        if data:
            self.location_cb.current(0)

    def validate_email(self, email):
        return "@" in email and "." in email and len(email) <= 255

    def validate_phone(self, phone):
        return bool(re.fullmatch(r"[0-9 +]{5,50}", phone))

    def validate_name(self, name):
        return bool(re.fullmatch(r"[A-Za-z \-]{1,255}", name))

    def validate_username(self, username):
        return bool(re.fullmatch(r"[A-Za-z0-9_]{3,50}", username))

    def save_user(self):
        loc_label = self.location_var.get()
        role = self.role_var.get()

        first = self.entries["First Name"].get().strip()
        last = self.entries["Last Name"].get().strip()
        email = self.entries["Email"].get().strip()
        phone = self.entries["Phone"].get().strip()
        username = self.entries["Username"].get().strip()
        password = self.entries["Password"].get().strip()

        if not all([loc_label, role, first, last, email, phone, username, password]):
            messagebox.showerror("Error", "All fields are required.")
            return

        if not self.validate_name(first):
            messagebox.showerror("Error", "Invalid first name.")
            return

        if not self.validate_name(last):
            messagebox.showerror("Error", "Invalid last name.")
            return

        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email address.")
            return

        if not self.validate_phone(phone):
            messagebox.showerror("Error", "Invalid phone number.")
            return

        if not self.validate_username(username):
            messagebox.showerror("Error", "Invalid username.")
            return

        if len(password) < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters.")
            return

        if len(password) > 72:
            messagebox.showerror("Error", "Password cannot exceed 72 characters.")
            return

        db = get_session()

        existing = db.query(User).filter(User.username == username).first()
        if existing:
            db.close()
            messagebox.showerror("Error", "Username already exists.")
            return

        location_id = int(self._location_map[loc_label])

        user = User(
            location_id=location_id,
            first_name=first,
            last_name=last,
            email=email,
            phone=phone,
            username=username,
            password_hash=bcrypt.hash(password[:72]),
            role=role,
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Staff user created successfully.")
        self.go_back()

    def go_back(self):
        from ui.user_management.users_home import UsersHomePage
        self.main_window.load_page(UsersHomePage)