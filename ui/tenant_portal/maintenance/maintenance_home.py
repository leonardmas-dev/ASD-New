import tkinter as tk
from tkinter import ttk

from backend.maintenance_service import MaintenanceService
from database.session import get_session


class MaintenanceHome(tk.Frame):
    """Tenant view of maintenance requests."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session
        tenant_id = self.session.tenant_id

        tk.Label(self, text="My Maintenance Requests", font=("Arial", 22)).pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Submit Request",
            width=20,
            command=self.open_submit_request
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="View Request History",
            width=20,
            command=self.open_history
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            self,
            text="Back to Dashboard",
            command=self.go_home
        ).pack(pady=10)

        # Table
        self.table = ttk.Treeview(
            self,
            columns=("desc", "priority", "status", "submitted"),
            show="headings",
        )
        self.table.heading("desc", text="Description")
        self.table.heading("priority", text="Priority")
        self.table.heading("status", text="Status")
        self.table.heading("submitted", text="Submitted At")
        self.table.pack(fill="both", expand=True, pady=10)

        self.load_requests()

    def load_requests(self):
        db = get_session()
        service = MaintenanceService(db)
        rows = service.get_requests_for_tenant(self.session.tenant_id)

        extracted = [
            (r["description"], r["priority"], r["status"], r["submitted_at"])
            for r in rows
        ]

        db.close()

        for row in extracted:
            self.table.insert("", "end", values=row)

    def open_submit_request(self):
        from ui.tenant_portal.maintenance.submit_request import SubmitRequest
        self.main_window.load_page(SubmitRequest)

    def open_history(self):
        from ui.tenant_portal.maintenance.view_requests import ViewMaintenanceRequestsPage
        self.main_window.load_page(ViewMaintenanceRequestsPage)

    def go_home(self):
        from ui.tenant_portal.tenant_dashboard import TenantDashboard
        self.main_window.load_page(TenantDashboard)