import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from backend.payment_service import PaymentService


class RecordPaymentPage(tk.Frame):
    """
    Finance Manager page to record a payment for a lease.
    """

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Record Payment", font=("Arial", 18, "bold")).pack(pady=10)

        self.service = PaymentService()

        # lease selection
        lease_frame = tk.Frame(self)
        lease_frame.pack(pady=10, fill="x")

        tk.Label(lease_frame, text="Select Lease").grid(row=0, column=0, sticky="w")

        self.lease_box = ttk.Combobox(lease_frame, width=60, state="readonly")
        self.lease_box.grid(row=0, column=1, padx=5)

        self.leases = self.service.get_active_leases()
        lease_display = []
        for l in self.leases:
            tenant = l.tenant
            apt = l.apartment
            loc = apt.location
            label = f"Lease #{l.lease_id} - {tenant.first_name} {tenant.last_name} - {loc.city} - Apt {apt.apartment_id}"
            lease_display.append(label)
        self.lease_box["values"] = lease_display

        # amount + due date
        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Amount Due (£)").grid(row=0, column=0, sticky="w")
        self.amount_due_entry = tk.Entry(form_frame)
        self.amount_due_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Amount Paid (£)").grid(row=1, column=0, sticky="w")
        self.amount_paid_entry = tk.Entry(form_frame)
        self.amount_paid_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Due Date (YYYY-MM-DD)").grid(row=2, column=0, sticky="w")
        self.due_date_entry = tk.Entry(form_frame)
        self.due_date_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Payment Date (optional, YYYY-MM-DD)").grid(row=3, column=0, sticky="w")
        self.payment_date_entry = tk.Entry(form_frame)
        self.payment_date_entry.grid(row=3, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Save Payment", command=self.save_payment).grid(row=0, column=0, padx=5)

        from ui.payments.payments_home import PaymentsHome
        tk.Button(btn_frame, text="Back", command=lambda: main_window.load_page(PaymentsHome)).grid(
            row=0, column=1, padx=5
        )

    def save_payment(self):
        # validate lease selection
        idx = self.lease_box.current()
        if idx == -1:
            messagebox.showerror("Error", "Please select a lease")
            return

        lease = self.leases[idx]

        # validate numeric fields
        try:
            amount_due = int(self.amount_due_entry.get().strip())
            amount_paid = int(self.amount_paid_entry.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Amounts must be whole numbers")
            return

        # parse dates
        try:
            due_date_str = self.due_date_entry.get().strip()
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid due date format")
            return

        payment_date = None
        payment_date_str = self.payment_date_entry.get().strip()
        if payment_date_str:
            try:
                payment_date = datetime.strptime(payment_date_str, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Error", "Invalid payment date format")
                return

        # record payment
        payment = self.service.record_payment(
            lease_id=lease.lease_id,
            amount_due=amount_due,
            amount_paid=amount_paid,
            due_date=due_date,
            payment_date=payment_date,
        )

        # simple alert for late payments
        if payment.is_late:
            messagebox.showwarning(
                "Late Payment",
                f"Payment marked as LATE.\nLate fee applied: £{payment.late_fee}",
            )
        else:
            messagebox.showinfo("Success", "Payment recorded successfully")