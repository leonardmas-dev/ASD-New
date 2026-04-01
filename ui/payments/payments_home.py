import tkinter as tk
from tkinter import ttk
from backend.payment_service import PaymentService
from database.session import get_session


class PaymentsHome(tk.Frame):
    """Staff overview of all payments."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Payments", font=("Arial", 22)).pack(pady=20)

        # navigation buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Create Payment",
            width=18,
            command=self.open_create_page
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Record Completed Payments",
            width=26,
            command=self.open_add_page
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="View Payment List",
            width=18,
            command=self.open_list_page
        ).grid(row=0, column=2, padx=5)

        # payments table
        self.table = ttk.Treeview(
            self,
            columns=(
                "tenant",
                "apartment",
                "amount_due",
                "amount_paid",
                "due_date",
                "payment_date",
                "status",
                "late_fee",
            ),
            show="headings",
        )

        for col, text in [
            ("tenant", "Tenant"),
            ("apartment", "Apartment"),
            ("amount_due", "Amount Due"),
            ("amount_paid", "Amount Paid"),
            ("due_date", "Due Date"),
            ("payment_date", "Payment Date"),
            ("status", "Status"),
            ("late_fee", "Late Fee"),
        ]:
            self.table.heading(col, text=text)

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

    def load_data(self):
        """Load all payment records into the table."""
        db = get_session()
        service = PaymentService(db)
        rows = service.get_all_payments()
        db.close()

        for r in rows:
            self.table.insert(
                "",
                "end",
                values=(
                    r["tenant_name"],
                    r["apartment_label"],
                    r["amount_due"],
                    r["amount_paid"],
                    r["due_date"],
                    r["payment_date"],
                    r["status"],
                    r["late_fee"],
                ),
            )

    def open_add_page(self):
        """Navigate to record payment page."""
        from ui.payments.record_payment_page import RecordPaymentPage
        self.main_window.load_page(lambda parent, mw: RecordPaymentPage(parent, mw))

    def open_create_page(self):
        """Navigate to add payment page."""
        from ui.payments.add_payment_page import AddPaymentPage
        self.main_window.load_page(lambda parent, mw: AddPaymentPage(parent, mw))

    def open_list_page(self):
        """Navigate to tenant payment history page."""
        from ui.payments.payment_history_page import PaymentHistoryPage
        self.main_window.load_page(lambda parent, mw: PaymentHistoryPage(parent, mw))