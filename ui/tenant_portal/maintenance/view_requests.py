import tkinter as tk
from tkinter import ttk

from database.session import get_session
from backend.maintenance_service import MaintenanceService


class ViewMaintenanceRequestsPage(tk.Frame):
    """Displays all maintenance requests submitted by the tenant."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.session = main_window.user_session
        tenant_id = self.session.tenant_id

        tk.Label(self, text="My Maintenance Requests", font=("Arial", 20, "bold")).pack(pady=20)

        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10)

        self.table = ttk.Treeview(
            table_frame,
            columns=("status", "date", "category", "priority", "description"),
            show="headings",
            height=15,
        )

        self.table.heading("status", text="Status")
        self.table.heading("date", text="Date")
        self.table.heading("category", text="Category")
        self.table.heading("priority", text="Priority")
        self.table.heading("description", text="Description")

        self.table.column("status", width=120)
        self.table.column("date", width=150)
        self.table.column("category", width=120)
        self.table.column("priority", width=80)
        self.table.column("description", width=350)

        self.table.pack(fill="both", expand=True)

        tk.Button(
            self,
            text="Back",
            command=self.go_back,
        ).pack(pady=20)

        self.load_requests()

    def load_requests(self):
        for row in self.table.get_children():
            self.table.delete(row)

        db = get_session()
        service = MaintenanceService(db)

        try:
            requests = service.get_requests_for_tenant(self.session.tenant_id)
        finally:
            db.close()

        for r in requests:
            self.table.insert(
                "",
                "end",
                values=(
                    r["status"],
                    r["created_at"],
                    r["category"],
                    r["priority"],
                    r["description"],
                ),
            )

    def go_back(self):
        from ui.tenant_portal.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(MaintenanceHome)