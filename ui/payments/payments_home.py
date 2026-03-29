import tkinter as tk


class PaymentsHome(tk.Frame):
    """
    Entry point for Finance Manager payment workflows.
    """

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Payments & Billing", font=("Arial", 18, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        from ui.payments.record_payment_page import RecordPaymentPage
        from ui.payments.payment_history_page import PaymentHistoryPage

        tk.Button(
            btn_frame,
            text="Record Payment",
            width=25,
            command=lambda: main_window.load_page(RecordPaymentPage),
        ).pack(pady=5)

        tk.Button(
            btn_frame,
            text="View Payment History",
            width=25,
            command=lambda: main_window.load_page(PaymentHistoryPage),
        ).pack(pady=5)