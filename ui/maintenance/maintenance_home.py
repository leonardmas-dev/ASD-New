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

        # buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Request",
            width=18,
            command=self.open_add_page
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Edit Request",
            width=18,
            command=self.open_edit_page
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="View Request List",
            width=18,
            command=self.open_list_page
        ).grid(row=0, column=2, padx=5)

        # table
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

    # load maintenance requests
    def load_data(self):
        db = get_session()
        service = MaintenanceService(db)
        rows = service.get_all_requests()

        # extract before closing session
        req_rows = []
        for r in rows:
            req_rows.append((
                r["tenant_name"],
                r["apartment_label"],
                r["description"],
                r["priority"],
                r["status"],
                r["submitted_at"],
            ))

        db.close()

        for row in req_rows:
            self.table.insert("", "end", values=row)

    # open add request page
    def open_add_page(self):
        from ui.maintenance.add_request_page import AddRequestPage
        self.main_window.load_page(AddRequestPage)

    # open edit request page
    def open_edit_page(self):
        from ui.maintenance.edit_request_page import EditRequestPage
        self.main_window.load_page(EditRequestPage)

    # open request list page
    def open_list_page(self):
        from ui.maintenance.request_list_page import RequestListPage
        self.main_window.load_page(RequestListPage)