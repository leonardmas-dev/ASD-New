import tkinter as tk


class TenantDashboard(tk.Frame):
    """
    Tenant main landing page.
    Acts as the central hub for all tenant portal modules.
    """

    def __init__(self, parent, main_window):
        super().__init__(parent)

        # Store reference to main window + session info
        self.main_window = main_window
        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id

        # --- Header ---
        tk.Label(self, text="Tenant Dashboard", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self, text="Welcome to your tenant portal.").pack(pady=5)

        # Optional: simple tenant identifier
        tk.Label(self, text=f"Logged in as Tenant ID: {self.tenant_id}").pack(pady=5)

        # --- Button Grid Container ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        # --- Module Navigation Buttons ---
        # Each button routes to a module home page (mirrors staff-side structure)
        tk.Button(
            btn_frame,
            text="Complaints",
            width=25,
            command=self.open_complaints_home,
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="Maintenance",
            width=25,
            command=self.open_maintenance_home,
        ).grid(row=0, column=1, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="Payments",
            width=25,
            command=self.open_payments_home,
        ).grid(row=1, column=0, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="My Lease",
            width=25,
            command=self.open_lease_view,
        ).grid(row=1, column=1, padx=10, pady=5)

    # --- Navigation Handlers ---
    # Each method loads the corresponding module home page.

    def open_complaints_home(self):
        from ui.tenant_portal.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(ComplaintsHome)

    def open_maintenance_home(self):
        from ui.tenant_portal.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(MaintenanceHome)

    def open_payments_home(self):
        from ui.tenant_portal.payments.payments_home import PaymentsHome
        self.main_window.load_page(PaymentsHome)

    def open_lease_view(self):
        from ui.tenant_portal.lease.lease_view import LeaseViewPage
        self.main_window.load_page(LeaseViewPage)