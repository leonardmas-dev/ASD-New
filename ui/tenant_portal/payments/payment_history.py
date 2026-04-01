# Student: Yaseen Sassi     StudentID: 24023127

import tkinter as tk
from tkinter import ttk

from backend.payment_service import PaymentService
from database.session import get_session


class TenantPaymentsHistoryPage(tk.Frame):
    """Tenant view of their payment history."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.session = main_window.user_session

        # Title
        header = tk.Frame(self)
        header.pack(fill="x", pady=10)

        tk.Label(header, text="My Payment History", font=("Arial", 22)).pack(side="left", padx=20)

        # Neighbour Comparison Summary
        summary_frame = tk.Frame(header)
        summary_frame.pack(side="right", padx=20)

        db = get_session()
        service = PaymentService(db)
        comparison = service.get_neighbour_comparison(self.session.tenant_id)
        db.close()

        tenant_total = comparison["tenant_total"]
        neighbours_avg = comparison["neighbours_avg"]

        summary_text = (
            f"Your Total Paid: £{tenant_total}\n"
            f"Neighbour Avg: £{neighbours_avg}"
        )

        tk.Label(
            summary_frame,
            text=summary_text,
            font=("Arial", 10),
            justify="right"
        ).pack()

        # Table
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10)

        self.table = ttk.Treeview(
            table_frame,
            columns=("due_date", "amount_due", "amount_paid", "status", "paid_at"),
            show="headings",
            height=15,
        )

        self.table.heading("due_date", text="Due Date")
        self.table.heading("amount_due", text="Amount Due (£)")
        self.table.heading("amount_paid", text="Amount Paid (£)")
        self.table.heading("status", text="Status")
        self.table.heading("paid_at", text="Paid At")

        self.table.column("due_date", width=150)
        self.table.column("amount_due", width=130)
        self.table.column("amount_paid", width=130)
        self.table.column("status", width=120)
        self.table.column("paid_at", width=150)

        self.table.pack(fill="both", expand=True)

        tk.Button(
            self,
            text="Back",
            command=self.go_back,
        ).pack(pady=20)

        self.load_history()

    def load_history(self):
        for row in self.table.get_children():
            self.table.delete(row)

        db = get_session()
        service = PaymentService(db)
        payments = service.get_payment_history_for_tenant(self.session.tenant_id)
        db.close()

        for p in payments:
            paid_at = p.paid_at.strftime("%Y-%m-%d") if p.paid_at else ""
            due_date = p.due_date.strftime("%Y-%m-%d") if p.due_date else ""

            self.table.insert(
                "",
                "end",
                values=(
                    due_date,
                    p.amount_due,
                    p.amount_paid or 0,
                    p.status,
                    paid_at,
                ),
            )

    def go_back(self):
        from ui.tenant_portal.payments.payments_home import PaymentsHome
        self.main_window.load_page(lambda parent, mw: PaymentsHome(parent, mw))