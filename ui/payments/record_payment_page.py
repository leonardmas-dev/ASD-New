import tkinter as tk
from tkinter import ttk, messagebox

from backend.payment_service import PaymentService
from database.session import get_session
from database.models import Payment, Lease, Tenant, Apartment


class RecordPaymentPage(tk.Frame):
    """Staff records a payment against an existing payment record."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window

        tk.Label(self, text="Record Payment", font=("Arial", 22)).pack(pady=20)

        top = tk.Frame(self)
        top.pack(pady=5)

        tk.Label(top, text="Select Payment:").pack(side="left", padx=5)

        self.payment_combo = ttk.Combobox(top, state="readonly", width=60)
        self.payment_combo.pack(side="left", padx=5)

        tk.Button(top, text="Load", command=self._load_selected).pack(side="left", padx=5)

        form = tk.Frame(self)
        form.pack(pady=15)

        tk.Label(form, text="Amount to Record:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.amount_entry = tk.Entry(form)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(self, text="Save Payment", command=self.save_payment).pack(pady=10)

        self._load_payments()

    def _load_payments(self):
        db = get_session()
        rows = (
            db.query(Payment, Lease, Tenant, Apartment)
            .join(Lease, Payment.lease_id == Lease.lease_id)
            .join(Tenant, Lease.tenant_id == Tenant.tenant_id)
            .join(Apartment, Lease.apartment_id == Apartment.apartment_id)
            .all()
        )
        db.close()

        self.payment_map = {}
        labels = []
        for pay, lease, tenant, apt in rows:
            label = (
                f"ID {pay.payment_id} | {tenant.first_name} {tenant.last_name} | "
                f"Due £{pay.amount_due} on {pay.due_date.strftime('%Y-%m-%d')} | Status {pay.status}"
            )
            labels.append(label)
            self.payment_map[label] = pay.payment_id

        self.payment_combo["values"] = labels

    def _load_selected(self):
        # kept simple: just focuses on amount entry; details already in combo text
        pass

    def save_payment(self):
        sel = self.payment_combo.get()
        if not sel:
            messagebox.showerror("Error", "Please select a payment.")
            return

        try:
            amount = int(self.amount_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Enter a valid amount.")
            return

        payment_id = self.payment_map[sel]

        db = get_session()
        service = PaymentService(db)
        ok = service.record_payment(payment_id, amount)
        db.close()

        if ok:
            messagebox.showinfo("Success", "Payment recorded.")
            self._load_payments()
        else:
            messagebox.showerror("Error", "Failed to record payment.")