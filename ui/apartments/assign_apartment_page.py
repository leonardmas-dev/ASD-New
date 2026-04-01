# Student: Thierno Batiga     StudentID: 24024769

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

from database.session import get_session
from database.models import Apartment, Tenant, Lease


class AssignApartmentPage(tk.Frame):
    """Create a lease: assign an apartment to a tenant."""

    def __init__(self, parent, main_window, apartment_id):
        super().__init__(parent)
        self.main_window = main_window
        self.apartment_id = apartment_id

        tk.Label(self, text="Assign Apartment to Tenant", font=("Arial", 22)).pack(pady=20)

        info_frame = tk.Frame(self)
        info_frame.pack(pady=5)

        self.apartment_label = tk.Label(info_frame, text="", font=("Arial", 12))
        self.apartment_label.pack()

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Select Tenant:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.tenant_combo = ttk.Combobox(form, state="readonly", width=40)
        self.tenant_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Lease Start Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.start_entry = tk.Entry(form, width=20)
        self.start_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Lease End Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.end_entry = tk.Entry(form, width=20)
        self.end_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Assign", width=18, command=self.assign).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", width=18, command=self.go_back).grid(row=0, column=1, padx=5)

        self._load_apartment()
        self._load_tenants()
        self._prefill_dates()

    def _load_apartment(self):
        db = get_session()
        apt = db.query(Apartment).filter(Apartment.apartment_id == self.apartment_id).first()
        db.close()

        if not apt:
            messagebox.showerror("Error", "Apartment not found.")
            self.go_back()
            return

        status = "Available" if apt.is_available else "Not Available"
        self.apartment_label.config(
            text=f"Apartment #{apt.apartment_id} | {apt.apartment_type} | Rent £{apt.monthly_rent} | {status}"
        )

        if not apt.is_available:
            messagebox.showinfo(
                "Info",
                "This apartment is currently marked as not available. "
                "Assigning a new lease will still be allowed but may overwrite occupancy logically.",
            )

    def _load_tenants(self):
        db = get_session()
        tenants = db.query(Tenant).filter(Tenant.is_active == True).all()
        db.close()

        self.tenant_map = {}
        values = []
        for t in tenants:
            label = f"{t.tenant_id} - {t.first_name} {t.last_name} ({t.email})"
            self.tenant_map[label] = t.tenant_id
            values.append(label)

        self.tenant_combo["values"] = values
        if values:
            self.tenant_combo.current(0)

    def _prefill_dates(self):
        today = datetime.utcnow().date()
        default_end = today + timedelta(days=365)
        self.start_entry.insert(0, today.isoformat())
        self.end_entry.insert(0, default_end.isoformat())

    def assign(self):
        tenant_label = self.tenant_combo.get().strip()
        start_raw = self.start_entry.get().strip()
        end_raw = self.end_entry.get().strip()

        if not tenant_label:
            messagebox.showerror("Error", "Please select a tenant.")
            return

        if tenant_label not in self.tenant_map:
            messagebox.showerror("Error", "Invalid tenant selected.")
            return

        try:
            start_date = datetime.strptime(start_raw, "%Y-%m-%d")
            end_date = datetime.strptime(end_raw, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Dates must be in format YYYY-MM-DD.")
            return

        if end_date <= start_date:
            messagebox.showerror("Error", "End date must be after start date.")
            return

        tenant_id = self.tenant_map[tenant_label]

        db = get_session()

        apt = db.query(Apartment).filter(Apartment.apartment_id == self.apartment_id).first()
        if not apt:
            db.close()
            messagebox.showerror("Error", "Apartment not found.")
            self.go_back()
            return

        lease = Lease(
            tenant_id=tenant_id,
            apartment_id=self.apartment_id,
            start_date=start_date,
            end_date=end_date,
            monthly_rent=apt.monthly_rent,
            deposit_amount=apt.monthly_rent,
            is_active=True,
        )

        apt.is_available = False

        db.add(lease)
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Apartment assigned and lease created.")
        self.go_back()

    def go_back(self):
        from ui.apartments.apartments_home import ApartmentsHome
        self.main_window.load_page(ApartmentsHome)