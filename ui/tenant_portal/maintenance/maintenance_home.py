import tkinter as tk


class MaintenanceHome(tk.Frame):
    """
    Module home page for tenant maintenance requests.
    Provides entry points for submitting and viewing requests.
    """

    def __init__(self, parent, main_window):
        super().__init__(parent)

        # Store reference to main window
        self.main_window = main_window

        # --- Header ---
        tk.Label(self, text="Maintenance", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self, text="Submit and track your maintenance requests.").pack(pady=5)

        # --- Navigation Buttons ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Submit a Request",
            width=25,
            command=self.open_submit_page,
        ).grid(row=0, column=0, padx=10, pady=5)

        tk.Button(
            btn_frame,
            text="View My Requests",
            width=25,
            command=self.open_view_page,
        ).grid(row=0, column=1, padx=10, pady=5)

        # Back to dashboard
        tk.Button(
            self,
            text="Back to Dashboard",
            command=self.go_home,
        ).pack(pady=20)

    # --- Navigation Handlers ---

    def open_submit_page(self):
        from ui.tenant_portal.maintenance.submit_request import SubmitMaintenanceRequestPage
        self.main_window.load_page(SubmitMaintenanceRequestPage)

    def open_view_page(self):
        from ui.tenant_portal.maintenance.view_requests import ViewMaintenanceRequestsPage
        self.main_window.load_page(ViewMaintenanceRequestsPage)

    def go_home(self):
        from ui.tenant_portal.dashboard.tenant_dashboard import TenantDashboard
        self.main_window.load_page(TenantDashboard)