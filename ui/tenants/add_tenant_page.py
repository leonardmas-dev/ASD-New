import tkinter as tk
from tkinter import messagebox

from database.session import get_session
from database.models import Tenant


class AddTenantPage(tk.Frame):
    """Create a new tenant."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Add Tenant", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        labels = ["First Name", "Last Name", "Email", "Phone"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(form, text=f"{label}:").grid(row=i, column=0, sticky="e")
            entry = tk.Entry(form, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[label] = entry

        tk.Button(self, text="Create Tenant", command=self.save).pack(pady=15)

    def save(self):
        first = self.entries["First Name"].get().strip()
        last = self.entries["Last Name"].get().strip()
        email = self.entries["Email"].get().strip()
        phone = self.entries["Phone"].get().strip()

        if not first or not last or not email:
            messagebox.showerror("Error", "Missing required fields.")
            return

        db = get_session()

        tenant = Tenant(
            first_name=first,
            last_name=last,
            email=email,
            phone=phone,
            is_active=True,
        )

        db.add(tenant)
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Tenant created.")