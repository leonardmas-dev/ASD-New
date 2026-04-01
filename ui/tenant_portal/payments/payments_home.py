import tkinter as tk

class PaymentsHome(tk.Frame):
    """Tenant payments module home page."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session

        tk.Label(self, text="My Payments", font=("Arial", 22)).pack(pady=20)
        tk.Label(self, text="View your payments and analyse your payment history.").pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Payment History",
            width=25,
            command=self.open_history,
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="Payment Graphs",
            width=25,
            command=self.open_graphs,
        ).grid(row=1, column=0, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="Make a Payment",
            width=25,
            command=self.open_make_payment,
        ).grid(row=2, column=0, padx=10, pady=5)

        tk.Button(
            self,
            text="Back to Dashboard",
            command=self.go_home,
        ).pack(pady=20)

    def open_history(self):
        from ui.tenant_portal.payments.payment_history import TenantPaymentsHistoryPage
        self.main_window.load_page(lambda parent, mw: TenantPaymentsHistoryPage(parent, mw))

    def open_graphs(self):
        from ui.tenant_portal.payments.payment_graphs import PaymentGraphs
        self.main_window.load_page(lambda parent, mw: PaymentGraphs(parent, mw))

    def open_make_payment(self):
        from ui.tenant_portal.payments.payment_make import TenantMakePaymentPage
        from backend.payment_service import PaymentService
        from database.session import get_session
        db = get_session()
        service = PaymentService(db)
        payments = service.get_payments_for_tenant(self.session.tenant_id)
        db.close()
        unpaid = next((p for p in payments if p["status"] == "Unpaid"), None)

        if unpaid:
            self.main_window.load_page(lambda parent, mw: TenantMakePaymentPage(parent, mw, unpaid))
        else:
            import tkinter.messagebox as messagebox
            messagebox.showinfo("No Payments", "You have no unpaid payments to make.")

    def go_home(self):
        from ui.tenant_portal.tenant_dashboard import TenantDashboard
        self.main_window.load_page(lambda parent, mw: TenantDashboard(parent, mw))