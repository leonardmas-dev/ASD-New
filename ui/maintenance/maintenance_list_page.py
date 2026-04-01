import tkinter as tk
from tkinter import ttk

from backend.maintenance_service import MaintenanceService
from database.session import get_session


class MaintenanceListPage(tk.Frame):
    """Read-only list of all maintenance requests."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Maintenance Request List", font=("Arial", 22)).pack(pady=20)

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.table = ttk.Treeview(
            container,
            columns=(
                "id",
                "tenant",
                "apartment",
                "priority",
                "status",
                "scheduled",
                "resolved",
                "time",
                "cost",
                "staff",
            ),
            show="headings",
            height=20,
        )

        headings = [
            ("id", "ID"),
            ("tenant", "Tenant"),
            ("apartment", "Apartment"),
            ("priority", "Priority"),
            ("status", "Status"),
            ("scheduled", "Scheduled Date"),
            ("resolved", "Resolved At"),
            ("time", "Time (hrs)"),
            ("cost", "Cost (£)"),
            ("staff", "Assigned Staff"),
        ]

        for col, text in headings:
            self.table.heading(col, text=text)
            self.table.column(col, width=140, anchor="center")

        vsb = ttk.Scrollbar(container, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=vsb.set)

        self.table.pack(side="left", fill="both", expand=True)
        vsb.pack(side="right", fill="y")

        tk.Button(
            self,
            text="Back",
            width=10,
            command=self.go_back,
        ).pack(pady=15)

        self.load_data()

    def load_data(self):
        db = get_session()
        service = MaintenanceService(db)
        rows = service.get_all_requests()
        db.close()

        for r in rows:
            scheduled = r["scheduled_date"].strftime("%Y-%m-%d %H:%M") if r["scheduled_date"] else ""
            resolved = r["resolved_at"].strftime("%Y-%m-%d %H:%M") if r["resolved_at"] else ""

            self.table.insert(
                "",
                "end",
                values=(
                    r["request_id"],
                    r["tenant_name"],
                    r["apartment_label"],
                    r["priority"],
                    r["status"],
                    scheduled,
                    resolved,
                    r["time_taken_hours"] if r["time_taken_hours"] is not None else "",
                    r["cost"] if r["cost"] is not None else "",
                    r["assigned_staff"],
                ),
            )

    def go_back(self):
        from ui.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(lambda parent, mw: MaintenanceHome(parent, mw))