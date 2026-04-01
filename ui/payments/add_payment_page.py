import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from backend.payment_service import PaymentService
from database.session import get_session
from database.models import Lease, Tenant, Apartment


class AddPaymentPage(tk.Frame):
    """Staff creates a new payment record for an active lease."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Create Payment", font=("Arial", 22)).pack(pady=20)

        # lease selector
        top = tk.Frame(self)
        top.pack(pady=10)

        tk.Label(top, text="Select Lease:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.lease_combo = ttk.Combobox(top, state="readonly", width=50)
        self.lease_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(top, text="Load", command=self._load_selected).grid(row=0, column=2, padx=5)

        # form fields
        form = tk.Frame(self)
        form.pack(pady=15)

        tk.Label(form, text="Rent Amount:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.rent_entry = tk.Entry(form, state="readonly")
        self.rent_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Due Date (YYYY-MM-DD):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.due_entry = tk.Entry(form)
        self.due_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self, text="Create Payment", command=self.save_payment).pack(pady=10)

        self._load_leases()

    def _load_leases(self):
        """Load active leases into dropdown."""
        db = get_session()
        rows = (
            db.query(Lease, Tenant, Apartment)
            .join(Tenant, Lease.tenant_id == Tenant.tenant_id)
            .join(Apartment, Lease.apartment_id == Apartment.apartment_id)
            .filter(Lease.is_active == True)
            .all()
        )
        db.close()

        self.lease_map = {}
        labels = []

        for lease, tenant, apt in rows:
            label = f"Lease {lease.lease_id} | {tenant.first_name} {tenant.last_name} | Apt {apt.apartment_id}"
            labels.append(label)
            self.lease_map[label] = lease.lease_id

        self.lease_combo["values"] = labels

    def _load_selected(self):
        """Load rent amount for selected lease."""
        sel = self.lease_combo.get()
        if not sel:
            return

        lease_id = self.lease_map[sel]

        db = get_session()
        lease = db.query(Lease).filter(Lease.lease_id == lease_id).first()
        rent = lease.apartment.monthly_rent
        db.close()

        self.rent_entry.config(state="normal")
        self.rent_entry.delete(0, tk.END)
        self.rent_entry.insert(0, str(rent))
        self.rent_entry.config(state="readonly")

    def save_payment(self):
        """Create a new payment record."""
        sel = self.lease_combo.get()
        if not sel:
            messagebox.showerror("Error", "Select a lease first.")
            return

        lease_id = self.lease_map[sel]

        try:
            due_date = datetime.strptime(self.due_entry.get().strip(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format.")
            return

        amount_due = int(self.rent_entry.get().strip())

        db = get_session()
        service = PaymentService(db)
        ok = service.create_payment(lease_id, amount_due, due_date)
        db.close()

        if ok:
            messagebox.showinfo("Success", "Payment created.")
            self.main_window.load_page(lambda parent, mw: AddPaymentPage(parent, mw))
        else:
            messagebox.showerror("Error", "Failed to create payment.")