import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database.session import get_session
from database.models import Lease


class EditLeasePage(tk.Frame):
    """Edit an existing lease."""

    def __init__(self, parent, main_window, lease_id):
        super().__init__(parent)

        self.lease_id = lease_id

        tk.Label(self, text="Edit Lease", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Monthly Rent:").grid(row=0, column=0, sticky="e")
        self.rent_entry = tk.Entry(form)
        self.rent_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Deposit:").grid(row=1, column=0, sticky="e")
        self.deposit_entry = tk.Entry(form)
        self.deposit_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Start Date:").grid(row=2, column=0, sticky="e")
        self.start_entry = tk.Entry(form)
        self.start_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="End Date:").grid(row=3, column=0, sticky="e")
        self.end_entry = tk.Entry(form)
        self.end_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form, text="Active (Yes/No):").grid(row=4, column=0, sticky="e")
        self.active_combo = ttk.Combobox(form, values=["Yes", "No"], state="readonly")
        self.active_combo.grid(row=4, column=1, padx=5, pady=5)

        tk.Button(self, text="Save Changes", command=self.save).pack(pady=15)

        self.load_data()

    def load_data(self):
        db = get_session()
        lease = db.query(Lease).filter(Lease.lease_id == self.lease_id).first()
        db.close()

        self.rent_entry.insert(0, lease.monthly_rent)
        self.deposit_entry.insert(0, lease.deposit_amount)
        self.start_entry.insert(0, lease.start_date.strftime("%Y-%m-%d"))
        self.end_entry.insert(0, lease.end_date.strftime("%Y-%m-%d"))
        self.active_combo.set("Yes" if lease.is_active else "No")

    def save(self):
        try:
            rent = int(self.rent_entry.get())
            deposit = int(self.deposit_entry.get())
            start = datetime.strptime(self.start_entry.get(), "%Y-%m-%d")
            end = datetime.strptime(self.end_entry.get(), "%Y-%m-%d")
            active = self.active_combo.get() == "Yes"
        except Exception:
            messagebox.showerror("Error", "Invalid input.")
            return

        db = get_session()
        lease = db.query(Lease).filter(Lease.lease_id == self.lease_id).first()

        lease.monthly_rent = rent
        lease.deposit_amount = deposit
        lease.start_date = start
        lease.end_date = end
        lease.is_active = active

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Lease updated.")