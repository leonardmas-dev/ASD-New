import tkinter as tk
from tkinter import ttk

from backend.maintenance_service import MaintenanceService
from database.session import get_session


class MaintenanceListPage(tk.Frame):
    """List of maintenance requests for selection."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Select Maintenance Request", font=("Arial", 22)).pack(pady=20)

        self.table = ttk.Treeview(
            self,
            columns=("id", "tenant", "apartment", "status"),
            show="headings",
        )

        for col, text in [
            ("id", "Request ID"),
            ("tenant", "Tenant"),
            ("apartment", "Apartment"),
            ("status", "Status"),
        ]:
            self.table.heading(col, text=text)

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

    def load_data(self):
        db = get_session()
        service = MaintenanceService(db)
        rows = service.get_all_requests()
        db.close()

        for r in rows:
            self.table.insert(
                "",
                "end",
                values=(
                    r["request_id"],
                    r["tenant_name"],
                    r["apartment_label"],
                    r["status"],
                ),
            )