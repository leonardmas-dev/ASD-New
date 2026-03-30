import tkinter as tk
from tkinter import messagebox

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from backend.payment_service import PaymentService


class TenantPaymentGraphsPage(tk.Frame):
    """
    Displays payment-related graphs:
    - Payment history
    - Tenant vs neighbours
    - Late payments per property
    """

    def __init__(self, parent, main_window):
        super().__init__(parent)

        # Store references
        self.main_window = main_window
        self.service = PaymentService()
        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id

        # --- Header ---
        tk.Label(self, text="Payment Graphs", font=("Arial", 18, "bold")).pack(pady=10)

        # --- Graph Selection Buttons ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Payment History", command=self.show_payment_history_graph).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Me vs Neighbours", command=self.show_neighbours_graph).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Late Payments per Property", command=self.show_late_payments_graph).grid(row=0, column=2, padx=5)

        # --- Matplotlib Figure Setup ---
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, pady=10)

        # Back navigation
        self.add_back_button()

    # --- Graph: Payment History ---
    def show_payment_history_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        payments = self.service.get_payment_history_for_tenant(self.tenant_id)
        if not payments:
            messagebox.showinfo("No Data", "No payments found.")
            return

        amounts = [p.amount_paid for p in payments]
        labels = [p.due_date.strftime("%Y-%m-%d") for p in payments]

        ax.plot(range(len(amounts)), amounts, marker="o")
        ax.set_title("Payment History")
        ax.set_xlabel("Payment Index")
        ax.set_ylabel("Amount Paid (£)")
        ax.set_xticks(range(len(labels)))
        ax.set_xticklabels(labels, rotation=45, ha="right")

        self.figure.tight_layout()
        self.canvas.draw()

    # --- Graph: Tenant vs Neighbours ---
    def show_neighbours_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        summary = self.service.get_neighbour_payment_summary_for_tenant(self.tenant_id)
        if not summary:
            messagebox.showinfo("No Data", "No neighbour data available.")
            return

        labels = ["You", "Neighbours Avg"]
        values = [summary["tenant_total"], summary["neighbours_avg"]]

        ax.bar(labels, values, color=["#3498db", "#95a5a6"])
        ax.set_title("Your Payments vs Neighbours")
        ax.set_ylabel("Total Amount Paid (£)")

        self.figure.tight_layout()
        self.canvas.draw()

    # --- Graph: Late Payments per Property ---
    def show_late_payments_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        data = self.service.get_late_payments_by_property_for_tenant(self.tenant_id)
        if not data:
            messagebox.showinfo("No Data", "No late payments found.")
            return

        labels = [str(d["apartment_id"]) for d in data]
        values = [d["late_count"] for d in data]

        ax.bar(labels, values, color="#e74c3c")
        ax.set_title("Late Payments per Property")
        ax.set_xlabel("Apartment ID")
        ax.set_ylabel("Late Payment Count")

        self.figure.tight_layout()
        self.canvas.draw()

    # --- Back Button ---
    def add_back_button(self):
        from ui.tenant_portal.payments.payments_home import PaymentsHome
        tk.Button(
            self,
            text="Back",
            command=lambda: self.main_window.load_page(PaymentsHome),
        ).pack(pady=20)