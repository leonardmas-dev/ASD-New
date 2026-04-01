# Student: Yaseen Sassi     StudentID: 24023127

import tkinter as tk
from tkinter import ttk

from backend.payment_service import PaymentService
from database.session import get_session

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PaymentGraphs(tk.Frame):
    """Tenant payment sequence graph (Payment 1, Payment 2, Payment 3...)."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.session = main_window.user_session

        header = tk.Frame(self)
        header.pack(fill="x", pady=10)

        tk.Label(header, text="Payment Summary", font=("Arial", 22)).pack(side="left", padx=20)

        tk.Button(
            header,
            text="Back",
            command=self.go_back,
            width=10
        ).pack(side="right", padx=20)

        # get payments in order
        db = get_session()
        service = PaymentService(db)
        sequence = service.get_payment_sequence_for_tenant(self.session.tenant_id)
        db.close()

        indexes = [row["index"] for row in sequence]
        paid = [row["paid"] for row in sequence]
        due = [row["due"] for row in sequence]

        # content frame for graph and table I will add
        content = tk.Frame(self)
        content.pack(fill="both", expand=True)

        # - Graph 
        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(indexes, paid, marker="o", color="green", label="Paid (£)", linewidth=2)
        ax.plot(indexes, due, marker="o", color="red", label="Due (£)", linestyle="--")

        ax.set_title("Payment Trend (Sequential)")
        ax.set_xlabel("Payment Number")
        ax.set_ylabel("Amount (£)")
        ax.grid(True)
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=content)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

        # - Table
        table = ttk.Treeview(
            content,
            columns=("index", "paid", "due"),
            show="headings",
            height=10,
        )

        table.heading("index", text="Payment #")
        table.heading("paid", text="Paid (£)")
        table.heading("due", text="Due (£)")

        table.column("index", width=120)
        table.column("paid", width=120)
        table.column("due", width=120)

        table.pack(pady=10, fill="both", expand=True)

        for row in sequence:
            table.insert("", "end", values=(row["index"], row["paid"], row["due"]))

    def go_back(self):
        from ui.tenant_portal.payments.payments_home import PaymentsHome
        self.main_window.load_page(lambda parent, mw: PaymentsHome(parent, mw))