import tkinter as tk


class TenantDashboard(tk.Frame):
    """Main tenant dashboard with navigation to tenant modules."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.session = main_window.user_session

        tk.Label(self, text="Tenant Dashboard", font=("Arial", 24)).pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        # My Lease
        tk.Button(
            btn_frame,
            text="My Lease",
            width=20,
            command=self.open_lease
        ).grid(row=0, column=0, padx=5, pady=5)

        # Payments
        tk.Button(
            btn_frame,
            text="Payments",
            width=20,
            command=self.open_payments
        ).grid(row=0, column=1, padx=5, pady=5)

        # Payment Graphs
        tk.Button(
            btn_frame,
            text="Payment Graphs",
            width=20,
            command=self.open_payment_graphs
        ).grid(row=1, column=0, padx=5, pady=5)

        # Maintenance
        tk.Button(
            btn_frame,
            text="Maintenance",
            width=20,
            command=self.open_maintenance
        ).grid(row=1, column=1, padx=5, pady=5)

        # Complaints
        tk.Button(
            btn_frame,
            text="Complaints",
            width=20,
            command=self.open_complaints
        ).grid(row=2, column=0, padx=5, pady=5)

    # Navigation methods
    def open_lease(self):
        from ui.tenant_portal.lease.lease_view import LeaseView
        self.main_window.load_page(LeaseView)

    def open_payments(self):
        from ui.tenant_portal.payments.payments_home import PaymentsHome
        self.main_window.load_page(PaymentsHome)

    def open_payment_graphs(self):
        from ui.tenant_portal.payments.payment_graphs import PaymentGraphs
        self.main_window.load_page(PaymentGraphs)

    def open_maintenance(self):
        from ui.tenant_portal.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(MaintenanceHome)

    def open_complaints(self):
        from ui.tenant_portal.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(ComplaintsHome)