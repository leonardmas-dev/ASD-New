import tkinter as tk
from tkinter import ttk

from backend.maintenance_service import MaintenanceService
from database.session import get_session


class MaintenanceHome(tk.Frame):
    """Staff overview of all maintenance requests."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Maintenance Requests", font=("Arial", 22)).pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Create Request",
            width=18,
            command=self.open_create_page,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Update Request",
            width=18,
            command=self.open_update_page,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="View Request List",
            width=18,
            command=self.open_list_page,
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            btn_frame,
            text="Refresh",
            width=12,
            command=self.refresh_table,
        ).grid(row=0, column=3, padx=5)

        self.table = ttk.Treeview(
            self,
            columns=("tenant", "apartment", "desc", "priority", "status", "submitted"),
            show="headings",
        )

        for col, text in [
            ("tenant", "Tenant"),
            ("apartment", "Apartment"),
            ("desc", "Description"),
            ("priority", "Priority"),
            ("status", "Status"),
            ("submitted", "Submitted At"),
        ]:
            self.table.heading(col, text=text)

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

    def load_data(self):
        db = get_session()
        service = MaintenanceService(db)
        rows = service.get_all_requests()

        extracted = [
            (
                r["tenant_name"],
                r["apartment_label"],
                r["description"],
                r["priority"],
                r["status"],
                r["submitted_at"],
            )
            for r in rows
        ]

        db.close()

        for row in extracted:
            self.table.insert("", "end", values=row)

    def refresh_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        self.load_data()

    def open_create_page(self):
        from ui.maintenance.create_request_page import CreateRequestPage
        self.main_window.load_page(CreateRequestPage)

    def open_update_page(self):
        from ui.maintenance.update_request_page import UpdateRequestPage
        self.main_window.load_page(UpdateRequestPage)

    def open_list_page(self):
        from ui.maintenance.maintenance_list_page import MaintenanceListPage
        self.main_window.load_page(MaintenanceListPage)