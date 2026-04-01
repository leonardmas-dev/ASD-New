import tkinter as tk
from tkinter import ttk

from backend.payment_service import PaymentService
from database.session import get_session


class PaymentGraphs(tk.Frame):
    """Tenant payment summary + neighbour comparison."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.session = main_window.user_session
        tenant_id = self.session.tenant_id

        db = get_session()
        service = PaymentService(db)

        monthly = service.get_monthly_payment_summary(tenant_id)
        compare = service.get_neighbour_comparison(tenant_id)

        db.close()

        tk.Label(self, text="Payment Summary", font=("Arial", 22)).pack(pady=20)

        table = ttk.Treeview(self, columns=("month", "paid", "due"), show="headings")
        table.heading("month", text="Month")
        table.heading("paid", text="Paid (£)")
        table.heading("due", text="Due (£)")
        table.pack(pady=10)

        for row in monthly:
            table.insert("", "end", values=(row["month"], row["paid"], row["due"]))

        tk.Label(self, text="Neighbour Comparison", font=("Arial", 18)).pack(pady=20)

        tk.Label(self, text=f"Your Total Paid: £{compare['tenant_total']}", font=("Arial", 14)).pack()
        tk.Label(self, text=f"Neighbour Average: £{compare['neighbours_avg']}", font=("Arial", 14)).pack()

        tk.Button(
            self,
            text="Back",
            command=lambda: self.go_back(main_window),
        ).pack(pady=20)

    def go_back(self, main_window):
        from ui.tenant_portal.payments.payments_home import PaymentsHome
        main_window.load_page(PaymentsHome)