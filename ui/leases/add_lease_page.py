import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database.session import get_session
from database.models import Tenant, Apartment, Lease


class AddLeasePage(tk.Frame):
    """Create a new lease."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Add Lease", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Tenant:").grid(row=0, column=0, sticky="e")
        self.tenant_combo = ttk.Combobox(form, state="readonly", width=35)
        self.tenant_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Apartment:").grid(row=1, column=0, sticky="e")
        self.apartment_combo = ttk.Combobox(form, state="readonly", width=35)
        self.apartment_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Monthly Rent (£):").grid(row=2, column=0, sticky="e")
        self.rent_entry = tk.Entry(form)
        self.rent_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="Deposit (£):").grid(row=3, column=0, sticky="e")
        self.deposit_entry = tk.Entry(form)
        self.deposit_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form, text="Start Date (YYYY-MM-DD):").grid(row=4, column=0, sticky="e")
        self.start_entry = tk.Entry(form)
        self.start_entry.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(form, text="End Date (YYYY-MM-DD):").grid(row=5, column=0, sticky="e")
        self.end_entry = tk.Entry(form)
        self.end_entry.grid(row=5, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Create Lease", width=18, command=self.save).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", width=10, command=self.go_back).grid(row=0, column=1, padx=5)

        self._load_dropdowns()

    def _load_dropdowns(self):
        db = get_session()

        tenants = db.query(Tenant).filter(Tenant.is_active == True).all()
        apartments = db.query(Apartment).filter(Apartment.is_active == True).all()

        db.close()

        self.tenant_map = {
            f"{t.tenant_id} - {t.first_name} {t.last_name}": t.tenant_id
            for t in tenants
        }

        self.apartment_map = {
            f"{a.apartment_id} - {a.location.city} ({a.apartment_type})": a.apartment_id
            for a in apartments
        }

        self.tenant_combo["values"] = list(self.tenant_map.keys())
        self.apartment_combo["values"] = list(self.apartment_map.keys())

    def save(self):
        try:
            tenant_id = self.tenant_map[self.tenant_combo.get()]
            apartment_id = self.apartment_map[self.apartment_combo.get()]
            rent = int(self.rent_entry.get())
            deposit = int(self.deposit_entry.get())
            start = datetime.strptime(self.start_entry.get(), "%Y-%m-%d")
            end = datetime.strptime(self.end_entry.get(), "%Y-%m-%d")
        except Exception:
            messagebox.showerror("Error", "Invalid input.")
            return

        db = get_session()

        lease = Lease(
            tenant_id=tenant_id,
            apartment_id=apartment_id,
            monthly_rent=rent,
            deposit_amount=deposit,
            start_date=start,
            end_date=end,
            is_active=True,
        )

        db.add(lease)
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Lease created.")

    def go_back(self):
        from ui.leases.leases_home import LeasesHome
        self.main_window.load_page(LeasesHome)