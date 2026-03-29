import tkinter as tk
from tkinter import ttk, messagebox

from backend.payment_service import PaymentService


class PaymentHistoryPage(tk.Frame):
    """
    Finance Manager page to view payment history per lease.
    """

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Payment History", font=("Arial", 18, "bold")).pack(pady=10)

        self.service = PaymentService()

        # lease selection
        lease_frame = tk.Frame(self)
        lease_frame.pack(pady=10, fill="x")

        tk.Label(lease_frame, text="Select Lease").grid(row=0, column=0, sticky="w")

        self.lease_box = ttk.Combobox(lease_frame, width=60, state="readonly")
        self.lease_box.grid(row=0, column=1, padx=5)

        self.leases = self.service.get_active_leases()
        lease_display = []
        for l in self.leases:
            tenant = l.tenant
            apt = l.apartment
            loc = apt.location
            label = f"Lease #{l.lease_id} - {tenant.first_name} {tenant.last_name} - {loc.city} - Apt {apt.apartment_id}"
            lease_display.append(label)
        self.lease_box["values"] = lease_display

        tk.Button(lease_frame, text="Load History", command=self.load_history).grid(row=0, column=2, padx=5)

        # table
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

        from ui.payments.payments_home import PaymentsHome
        tk.Button(self, text="Back", command=lambda: main_window.load_page(PaymentsHome)).pack(pady=10)

    def load_history(self):
        idx = self.lease_box.current()
        if idx == -1:
            messagebox.showerror("Error", "Please select a lease")
            return

        lease = self.leases[idx]

        for row in self.table.get_children():
            self.table.delete(row)

        payments = self.service.get_payment_history_for_lease(lease.lease_id)

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