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

        # buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Payment",
            width=18,
            command=self.open_add_page
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="View Payment List",
            width=18,
            command=self.open_list_page
        ).grid(row=0, column=2, padx=5)

        # table
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

    # load payments into table
    def load_data(self):
        db = get_session()
        service = PaymentService(db)
        rows = service.get_all_payments()

        # extract before closing session
        payment_rows = []
        for r in rows:
            payment_rows.append((
                r["tenant_name"],
                r["apartment_label"],
                r["amount_due"],
                r["amount_paid"],
                r["due_date"],
                r["payment_date"],
                r["status"],
                r["late_fee"],
            ))

        db.close()

        for row in payment_rows:
            self.table.insert("", "end", values=row)

    # open add payment page
    def open_add_page(self):
        from ui.payments.record_payment_page import RecordPaymentPage
        self.main_window.load_page(RecordPaymentPage)

    # open payment list page
    def open_list_page(self):
        from ui.payments.payment_history_page import PaymentHistoryPage
        self.main_window.load_page(PaymentHistoryPage)