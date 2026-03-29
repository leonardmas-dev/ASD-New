import tkinter as tk
from tkinter import ttk

from backend.payment_service import PaymentService


class TenantPaymentsHistoryPage(tk.Frame):

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.service = PaymentService()

        tk.Label(self, text="My Payment History", font=("Arial", 18, "bold")).pack(pady=20)

        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id

        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10)

        self.table = ttk.Treeview(
            table_frame,
            columns=("due", "paid", "status", "late", "late_fee"),
            show="headings",
            height=15,
        )

        self.table.heading("due", text="Due (£)")
        self.table.heading("paid", text="Paid (£)")
        self.table.heading("status", text="Status")
        self.table.heading("late", text="Late?")
        self.table.heading("late_fee", text="Late Fee (£)")

        self.table.pack(fill="both", expand=True)

        from ui.tenant_portal.tenant_payments_page import TenantPaymentsPage
        tk.Button(
            self,
            text="Back",
            command=lambda: self.main_window.load_page(TenantPaymentsPage),
        ).pack(pady=10)

        self.load_history()

    def load_history(self):
        for row in self.table.get_children():
            self.table.delete(row)

        payments = self.service.get_payment_history_for_tenant(self.tenant_id)

        for p in payments:
            self.table.insert(
                "",
                "end",
                values=(
                    p.amount_due,
                    p.amount_paid,
                    p.status,
                    "Yes" if p.is_late else "No",
                    p.late_fee or 0,
                ),
            )