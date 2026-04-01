# Student: Yaseen Sassi     StudentID: 24023127

import tkinter as tk
from tkinter import ttk

from backend.payment_service import PaymentService
from database.session import get_session
from database.models import Tenant


class PaymentHistoryPage(tk.Frame):
    """Staff view of payment history for a selected tenant."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Payment History", font=("Arial", 22)).pack(pady=20)

        # tenant selector
        top = tk.Frame(self)
        top.pack(pady=5)

        tk.Label(top, text="Tenant:").pack(side="left", padx=5)

        self.tenant_combo = ttk.Combobox(top, state="readonly", width=30)
        self.tenant_combo.pack(side="left", padx=5)

        tk.Button(top, text="Load", command=self.load_history).pack(side="left", padx=5)

        # table for payment records
        self.table = ttk.Treeview(
            self,
            columns=("amount_due", "amount_paid", "due_date", "payment_date", "status", "late_fee"),
            show="headings",
        )

        for col, text in [
            ("amount_due", "Amount Due"),
            ("amount_paid", "Amount Paid"),
            ("due_date", "Due Date"),
            ("payment_date", "Payment Date"),
            ("status", "Status"),
            ("late_fee", "Late Fee"),
        ]:
            self.table.heading(col, text=text)

        self.table.pack(fill="both", expand=True, pady=10)

        self._load_tenants()

    def _load_tenants(self):
        """Load active tenants into dropdown."""
        db = get_session()
        tenants = db.query(Tenant).filter(Tenant.is_active == True).all()
        db.close()

        self.tenant_map = {}
        names = []

        for t in tenants:
            label = f"{t.tenant_id} - {t.first_name} {t.last_name}"
            names.append(label)
            self.tenant_map[label] = t.tenant_id

        self.tenant_combo["values"] = names

    def load_history(self):
        """Load payment history for selected tenant."""
        sel = self.tenant_combo.get()
        if not sel:
            return

        tenant_id = self.tenant_map[sel]

        db = get_session()
        service = PaymentService(db)
        rows = service.get_payments_for_tenant(tenant_id)
        db.close()

        # clear table
        self.table.delete(*self.table.get_children())

        # insert rows
        for r in rows:
            self.table.insert(
                "",
                "end",
                values=(
                    r["amount_due"],
                    r["amount_paid"],
                    r["due_date"],
                    r["payment_date"],
                    r["status"],
                    r["late_fee"],
                ),
            )