import tkinter as tk
from tkinter import ttk, messagebox

from database.session import get_session
from database.models import Tenant


class EditTenantPage(tk.Frame):
    """Edit an existing tenant."""

    def __init__(self, parent, main_window, tenant_id):
        super().__init__(parent)

        self.tenant_id = tenant_id

        tk.Label(self, text="Edit Tenant", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        labels = ["First Name", "Last Name", "Email", "Phone"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form, text=f"{label}:").grid(row=i, column=0, sticky="e")
            entry = tk.Entry(form, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        tk.Label(form, text="Active (Yes/No):").grid(row=4, column=0, sticky="e")
        self.active_combo = ttk.Combobox(form, values=["Yes", "No"], state="readonly")
        self.active_combo.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(self, text="Save Changes", command=self.save).pack(pady=15)

        self.load_data()

    def load_data(self):
        db = get_session()
        t = db.query(Tenant).filter(Tenant.tenant_id == self.tenant_id).first()
        db.close()

        self.entries["First Name"].insert(0, t.first_name)
        self.entries["Last Name"].insert(0, t.last_name)
        self.entries["Email"].insert(0, t.email)
        self.entries["Phone"].insert(0, t.phone or "")
        self.active_combo.set("Yes" if t.is_active else "No")

    def save(self):
        first = self.entries["First Name"].get().strip()
        last = self.entries["Last Name"].get().strip()
        email = self.entries["Email"].get().strip()
        phone = self.entries["Phone"].get().strip()
        active = self.active_combo.get() == "Yes"

        if not first or not last or not email:
            messagebox.showerror("Error", "Missing required fields.")
            return

        db = get_session()
        t = db.query(Tenant).filter(Tenant.tenant_id == self.tenant_id).first()

        t.first_name = first
        t.last_name = last
        t.email = email
        t.phone = phone
        t.is_active = active

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Tenant updated.")