import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from backend.payment_service import PaymentService
from database.session import get_session


class TenantPaymentsMakePage(tk.Frame):
    """Tenant page for submitting a payment."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id

        db = get_session()
        self.service = PaymentService(db)

        # Get active lease
        self.lease = self.service.get_current_active_lease_for_tenant(self.tenant_id)

        tk.Label(self, text="Make a Payment", font=("Arial", 20, "bold")).pack(pady=20)

        if not self.lease:
            tk.Label(self, text="No active lease found. You cannot make a payment.").pack(pady=10)
            db.close()
            self.add_back_button()
            return

        apt = self.lease.apartment
        loc = apt.location

        tk.Label(
            self,
            text=f"Lease #{self.lease.lease_id} — {loc.city} — Apt {apt.apartment_id}",
            font=("Arial", 12)
        ).pack(pady=5)

        form = tk.Frame(self)
        form.pack(pady=10)

        # Amount
        tk.Label(form, text="Amount to Pay (£)").grid(row=0, column=0, sticky="w")
        self.amount_entry = tk.Entry(form)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        # Due date
        tk.Label(form, text="Due Date (YYYY-MM-DD)").grid(row=1, column=0, sticky="w")
        self.due_entry = tk.Entry(form)
        self.due_entry.grid(row=1, column=1, padx=5, pady=5)

        # Card fields
        tk.Label(form, text="Card Number").grid(row=2, column=0, sticky="w")
        self.card_entry = tk.Entry(form)
        self.card_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="Expiry (MM/YY)").grid(row=3, column=0, sticky="w")
        self.expiry_entry = tk.Entry(form)
        self.expiry_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form, text="CVV").grid(row=4, column=0, sticky="w")
        self.cvv_entry = tk.Entry(form, show="*")
        self.cvv_entry.grid(row=4, column=1, padx=5, pady=5)

        btns = tk.Frame(self)
        btns.pack(pady=15)

        tk.Button(btns, text="Submit Payment", command=self.submit_payment).grid(row=0, column=0, padx=5)
        self.add_back_button(btns)

        db.close()

    def submit_payment(self):
        if not self.lease:
            return

        # Amount
        try:
            amount = float(self.amount_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number.")
            return

        # Due date
        try:
            due_date = datetime.strptime(self.due_entry.get().strip(), "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid due date format.")
            return

        # Card details
        card = self.card_entry.get().strip()
        expiry = self.expiry_entry.get().strip()
        cvv = self.cvv_entry.get().strip()

        db = get_session()
        service = PaymentService(db)

        payment = service.tenant_make_payment(
            tenant_id=self.tenant_id,
            lease_id=self.lease.lease_id,
            amount_due=amount,
            amount_paid=amount,
            due_date=due_date,
            card_number=card,
            expiry=expiry,
            cvv=cvv,
        )

        db.close()

        if not payment:
            messagebox.showerror("Payment Failed", "Invalid card details.")
            return

        if payment.is_late:
            messagebox.showwarning(
                "Late Payment",
                f"Payment recorded but marked as LATE.\nLate fee applied: £{payment.late_fee}"
            )
        else:
            messagebox.showinfo("Success", "Payment recorded successfully.")

    def add_back_button(self, parent=None):
        from ui.tenant_portal.payments.payments_home import PaymentsHome

        container = parent if parent else self
        tk.Button(
            container,
            text="Back",
            command=lambda: self.main_window.load_page(PaymentsHome),
        ).pack(pady=20)