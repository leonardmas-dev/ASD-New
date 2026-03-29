import tkinter as tk
from tkinter import messagebox
from datetime import datetime

from backend.payment_service import PaymentService


class TenantPaymentsMakePage(tk.Frame):

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.service = PaymentService()

        tk.Label(self, text="Make a Payment", font=("Arial", 18, "bold")).pack(pady=20)

        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id

        self.lease = self.service.get_current_active_lease_for_tenant(self.tenant_id)

        if not self.lease:
            tk.Label(self, text="No active lease found. You cannot make a payment at this time.").pack(pady=10)
            return

        apt = self.lease.apartment
        loc = apt.location

        info_text = f"Lease #{self.lease.lease_id} - {loc.city} - Apartment {apt.apartment_id}"
        tk.Label(self, text=info_text).pack(pady=5)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Amount to Pay (£)").grid(row=0, column=0, sticky="w")
        self.amount_entry = tk.Entry(form_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Due Date (YYYY-MM-DD)").grid(row=1, column=0, sticky="w")
        self.due_date_entry = tk.Entry(form_frame)
        self.due_date_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Card Number").grid(row=2, column=0, sticky="w")
        self.card_number_entry = tk.Entry(form_frame)
        self.card_number_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Expiry (MM/YY)").grid(row=3, column=0, sticky="w")
        self.expiry_entry = tk.Entry(form_frame)
        self.expiry_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="CVV").grid(row=4, column=0, sticky="w")
        self.cvv_entry = tk.Entry(form_frame, show="*")
        self.cvv_entry.grid(row=4, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Submit Payment", command=self.submit_payment).grid(row=0, column=0, padx=5)

        from ui.tenant_portal.tenant_payments_page import TenantPaymentsPage
        tk.Button(btn_frame, text="Back",
                  command=lambda: self.main_window.load_page(TenantPaymentsPage)).grid(row=0, column=1, padx=5)

    def submit_payment(self):
        if not self.lease:
            return

        try:
            amount = int(self.amount_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Amount must be a whole number")
            return

        due_str = self.due_date_entry.get().strip()
        try:
            due_date = datetime.strptime(due_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid due date format")
            return

        card_number = self.card_number_entry.get().strip()
        expiry = self.expiry_entry.get().strip()
        cvv = self.cvv_entry.get().strip()

        payment = self.service.tenant_make_payment(
            tenant_id=self.tenant_id,
            lease_id=self.lease.lease_id,
            amount_due=amount,
            amount_paid=amount,
            due_date=due_date,
            card_number=card_number,
            expiry=expiry,
            cvv=cvv,
        )

        if payment is None:
            messagebox.showerror("Payment Failed", "Card details are invalid. Please check and try again.")
            return

        if payment.is_late:
            messagebox.showwarning(
                "Late Payment",
                f"Payment recorded but marked as LATE.\nLate fee applied: £{payment.late_fee}",
            )
        else:
            messagebox.showinfo("Success", "Payment recorded successfully")