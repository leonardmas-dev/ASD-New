import tkinter as tk


class PaymentsHome(tk.Frame):
    """Tenant payments module home page."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session

        tk.Label(self, text="Payments", font=("Arial", 20, "bold")).pack(pady=20)
        tk.Label(self, text="Manage your payments and view your payment history.").pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Make a Payment",
            width=25,
            command=self.open_make_payment,
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="Payment History",
            width=25,
            command=self.open_history,
        ).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="Payment Graphs",
            width=25,
            command=self.open_graphs,
        ).grid(row=1, column=0, columnspan=2, pady=10)

        tk.Button(
            self,
            text="Back to Dashboard",
            command=self.go_home,
        ).pack(pady=20)

    def open_make_payment(self):
        from ui.tenant_portal.payments.payment_make import TenantPaymentsMakePage
        self.main_window.load_page(TenantPaymentsMakePage)

    def open_history(self):
        from ui.tenant_portal.payments.payment_history import TenantPaymentsHistoryPage
        self.main_window.load_page(TenantPaymentsHistoryPage)

    def open_graphs(self):
        from ui.tenant_portal.payments.payment_graphs import PaymentGraphs
        self.main_window.load_page(PaymentGraphs)

    def go_home(self):
        from ui.tenant_portal.tenant_dashboard import TenantDashboard
        self.main_window.load_page(TenantDashboard)