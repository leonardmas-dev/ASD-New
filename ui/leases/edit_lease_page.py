import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database.session import get_session
from database.models import Lease, Tenant, Apartment


class EditLeasePage(tk.Frame):
    """Staff updates an existing lease."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.current_lease_id = None

        tk.Label(self, text="Edit Lease", font=("Arial", 22)).pack(pady=20)

        select_frame = tk.Frame(self)
        select_frame.pack(pady=5)

        tk.Label(select_frame, text="Select Lease:").grid(row=0, column=0, sticky="e")
        self.lease_combo = ttk.Combobox(select_frame, state="readonly", width=45)
        self.lease_combo.grid(row=0, column=1, padx=5, pady=5)
        self.lease_combo.bind("<<ComboboxSelected>>", self.on_select)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="e")
        self.start_entry = tk.Entry(form)
        self.start_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="e")
        self.end_entry = tk.Entry(form)
        self.end_entry.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Save Changes", width=18, command=self.save).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", width=10, command=self.go_back).grid(row=0, column=1, padx=5)

        self._load_leases()

    def _load_leases(self):
        db = get_session()
        rows = (
            db.query(Lease, Tenant, Apartment)
            .join(Tenant, Lease.tenant_id == Tenant.tenant_id)
            .join(Apartment, Lease.apartment_id == Apartment.apartment_id)
            .all()
        )
        db.close()

        self.lease_map = {
            f"{l.lease_id} - {t.first_name} {t.last_name} - Apt {a.apartment_id} ({'Active' if l.is_active else 'Inactive'})":
                l.lease_id
            for l, t, a in rows
        }

        self.lease_combo["values"] = list(self.lease_map.keys())

    def on_select(self, event=None):
        label = self.lease_combo.get()
        if not label:
            return

        self.current_lease_id = self.lease_map.get(label)
        if not self.current_lease_id:
            return

        db = get_session()
        lease = db.query(Lease).filter(Lease.lease_id == self.current_lease_id).first()
        db.close()

        if not lease:
            messagebox.showerror("Error", "Lease not found.")
            return

        self.start_entry.delete(0, tk.END)
        self.start_entry.insert(0, lease.start_date.strftime("%Y-%m-%d"))

        self.end_entry.delete(0, tk.END)
        self.end_entry.insert(0, lease.end_date.strftime("%Y-%m-%d"))

    def save(self):
        if not self.current_lease_id:
            messagebox.showerror("Error", "Select a lease first.")
            return

        try:
            start = datetime.strptime(self.start_entry.get(), "%Y-%m-%d")
            end = datetime.strptime(self.end_entry.get(), "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Error", "Invalid input.")
            return

        db = get_session()
        lease = db.query(Lease).filter(Lease.lease_id == self.current_lease_id).first()

        if not lease:
            db.close()
            messagebox.showerror("Error", "Lease not found.")
            return

        lease.start_date = start
        lease.end_date = end

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Lease updated.")

    def go_back(self):
        from ui.leases.leases_home import LeasesHome
        self.main_window.load_page(LeasesHome)