import tkinter as tk
from tkinter import messagebox

from backend.payment_service import PaymentService
from database.session import get_session


class TenantMakePaymentPage(tk.Frame):
    """Tenant makes a payment (simulated card)."""

    def __init__(self, parent, main_window, payment):
        super().__init__(parent)

        self.main_window = main_window
        self.payment = payment  

        tk.Label(self, text="Make Payment", font=("Arial", 22)).pack(pady=20)

        # Payment summary
        summary = tk.Frame(self)
        summary.pack(pady=10)

        tk.Label(summary, text=f"Amount Due: £{self.payment['amount_due']}", font=("Arial", 14)).pack()
        tk.Label(summary, text=f"Status: {self.payment['status']}", font=("Arial", 12)).pack()

        # Here I have basically just simulated a card payment with fake details
        card_frame = tk.LabelFrame(self, text="Card Details (Simulated)", padx=10, pady=10)
        card_frame.pack(pady=20)

        # card holder
        tk.Label(card_frame, text="Card Holder Name:").grid(row=0, column=0, sticky="w")
        entry_name = tk.Entry(card_frame, width=30)
        entry_name.insert(0, "John Doe")
        entry_name.config(state="disabled")
        entry_name.grid(row=0, column=1, padx=5, pady=5)

        # card number
        tk.Label(card_frame, text="Card Number:").grid(row=1, column=0, sticky="w")
        entry_number = tk.Entry(card_frame, width=30)
        entry_number.insert(0, "0000 0000 0000 0000")
        entry_number.config(state="disabled")
        entry_number.grid(row=1, column=1, padx=5, pady=5)

        # CVV
        tk.Label(card_frame, text="CVV:").grid(row=2, column=0, sticky="w")
        entry_cvv = tk.Entry(card_frame, width=10)
        entry_cvv.insert(0, "000")
        entry_cvv.config(state="disabled")
        entry_cvv.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # expiry
        tk.Label(card_frame, text="Expiry:").grid(row=3, column=0, sticky="w")
        entry_exp = tk.Entry(card_frame, width=10)
        entry_exp.insert(0, "01/30")
        entry_exp.config(state="disabled")
        entry_exp.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # pay button
        tk.Button(
            self,
            text="Pay Now",
            width=20,
            bg="#4CAF50",
            fg="white",
            command=self.make_payment
        ).pack(pady=20)

        # back button
        tk.Button(
            self,
            text="Back",
            command=self.go_back
        ).pack(pady=10)

    def make_payment(self):
        db = get_session()
        service = PaymentService(db)

        ok = service.record_payment(
            payment_id=self.payment["payment_id"],
            amount_paid=self.payment["amount_due"]
        )

        db.close()

        if ok:
            messagebox.showinfo("Success", "Payment completed successfully.")
            from ui.tenant_portal.payments.payments_home import PaymentsHome
            self.main_window.load_page(lambda parent, mw: PaymentsHome(parent, mw))
        else:
            messagebox.showerror("Error", "Payment failed.")

    def go_back(self):
        from ui.tenant_portal.payments.payments_home import PaymentsHome
        self.main_window.load_page(lambda parent, mw: PaymentsHome(parent, mw))