# Student: Yaseen Sassi     StudentID: 24023127

import tkinter as tk
from tkinter import ttk, messagebox
import re
from database.session import get_session
from database.models import User, Location
from passlib.hash import bcrypt

ROLES = ["FrontDesk", "FinanceManager", "MaintenanceStaff", "Manager"]

class EditUserPage(tk.Frame):
    """Edit staff user account with full validation."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.current_user_id = None

        tk.Label(self, text="Edit Staff User", font=("Arial", 22)).pack(pady=20)

        select_frame = tk.Frame(self)
        select_frame.pack(pady=5)

        tk.Label(select_frame, text="Select User:").grid(row=0, column=0, sticky="e")
        self.user_combo = ttk.Combobox(select_frame, state="readonly", width=45)
        self.user_combo.grid(row=0, column=1, padx=5, pady=5)
        self.user_combo.bind("<<ComboboxSelected>>", self.on_select)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Location:").grid(row=0, column=0, sticky="e", padx=5, pady=3)
        self.location_var = tk.StringVar()
        self.location_cb = ttk.Combobox(form, textvariable=self.location_var, state="readonly", width=30)
        self.location_cb.grid(row=0, column=1, padx=5, pady=3)

        labels = [
            "First Name", "Last Name", "Email", "Phone",
            "Username", "New Password (optional)",
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

        self.active_var = tk.BooleanVar()
        tk.Checkbutton(form, text="Active", variable=self.active_var).grid(
            row=len(labels)+2, column=1, sticky="w", pady=5
        )

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Save Changes", width=18, command=self.save_changes).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", width=18, command=self.go_back).grid(row=0, column=1, padx=5)

        self.load_locations()
        self.load_users()

    def load_locations(self):
        db = get_session()
        locations = db.query(Location).filter(Location.is_active == True).all()
        db.close()

        data = [(str(loc.location_id), f"{loc.name} - {loc.city}") for loc in locations]
        self.location_cb["values"] = [label for _, label in data]
        self._location_map = {label: loc_id for loc_id, label in data}

    def load_users(self):
        db = get_session()
        users = db.query(User).all()
        db.close()

        self.user_map = {
            f"{u.user_id} - {u.first_name} {u.last_name} ({u.role})": u.user_id
            for u in users
        }

        self.user_combo["values"] = list(self.user_map.keys())

    def on_select(self, event=None):
        label = self.user_combo.get()
        if not label:
            return

        self.current_user_id = self.user_map.get(label)
        if not self.current_user_id:
            return

        db = get_session()
        user = db.query(User).filter(User.user_id == self.current_user_id).first()
        db.close()

        if not user:
            messagebox.showerror("Error", "User not found.")
            return

        for label, loc_id in self._location_map.items():
            if loc_id == user.location_id:
                self.location_var.set(label)
                break

        self.entries["First Name"].delete(0, tk.END)
        self.entries["First Name"].insert(0, user.first_name)

        self.entries["Last Name"].delete(0, tk.END)
        self.entries["Last Name"].insert(0, user.last_name)

        self.entries["Email"].delete(0, tk.END)
        self.entries["Email"].insert(0, user.email)

        self.entries["Phone"].delete(0, tk.END)
        self.entries["Phone"].insert(0, user.phone)

        self.entries["Username"].delete(0, tk.END)
        self.entries["Username"].insert(0, user.username)

        self.entries["New Password (optional)"].delete(0, tk.END)

        if user.role in ROLES:
            self.role_var.set(user.role)
        else:
            self.role_var.set(ROLES[0])

        self.active_var.set(user.is_active)

    def validate_email(self, email):
        return "@" in email and "." in email and len(email) <= 255

    def validate_phone(self, phone):
        return bool(re.fullmatch(r"[0-9 +]{5,50}", phone))

    def validate_name(self, name):
        return bool(re.fullmatch(r"[A-Za-z \-]{1,255}", name))

    def validate_username(self, username):
        return bool(re.fullmatch(r"[A-Za-z0-9_]{3,50}", username))

    def save_changes(self):
        if not self.current_user_id:
            messagebox.showerror("Error", "Select a user first.")
            return

        loc_label = self.location_var.get()
        role = self.role_var.get()

        first = self.entries["First Name"].get().strip()
        last = self.entries["Last Name"].get().strip()
        email = self.entries["Email"].get().strip()
        phone = self.entries["Phone"].get().strip()
        username = self.entries["Username"].get().strip()
        new_password = self.entries["New Password (optional)"].get().strip()
        is_active = self.active_var.get()

        if not all([loc_label, role, first, last, email, phone, username]):
            messagebox.showerror("Error", "All fields except password are required.")
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

        if new_password:
            if len(new_password) < 6:
                messagebox.showerror("Error", "Password must be at least 6 characters.")
                return
            if len(new_password) > 72:
                messagebox.showerror("Error", "Password cannot exceed 72 characters.")
                return

        db = get_session()
        user = db.query(User).filter(User.user_id == self.current_user_id).first()

        if not user:
            db.close()
            messagebox.showerror("Error", "User not found.")
            return

        existing = (
            db.query(User)
            .filter(User.username == username, User.user_id != self.current_user_id)
            .first()
        )
        if existing:
            db.close()
            messagebox.showerror("Error", "Username already exists.")
            return

        location_id = int(self._location_map[loc_label])

        user.location_id = location_id
        user.first_name = first
        user.last_name = last
        user.email = email
        user.phone = phone
        user.username = username
        user.role = role
        user.is_active = is_active

        if new_password:
            user.password_hash = bcrypt.hash(new_password[:72])

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Staff user updated successfully.")
        self.go_back()

    def go_back(self):
        from ui.user_management.users_home import UsersHomePage
        self.main_window.load_page(UsersHomePage)