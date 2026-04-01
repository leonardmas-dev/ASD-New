# Student: Ishak Askar    StudentID: 24023614

import tkinter as tk
from tkinter import ttk

from backend.complaint_service import ComplaintService
from database.session import get_session


class ComplaintListPage(tk.Frame):
    """Read-only list of complaints."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Complaint List", font=("Arial", 22)).pack(pady=20)

        # table
        self.table = ttk.Treeview(
            self,
            columns=("id", "tenant", "apartment", "status"),
            show="headings",
        )

        for col, text in [
            ("id", "Complaint ID"),
            ("tenant", "Tenant"),
            ("apartment", "Apartment"),
            ("status", "Status"),
        ]:
            self.table.heading(col, text=text)

        self.table.pack(fill="both", expand=True, pady=10)

        tk.Button(
            self,
            text="Back",
            width=10,
            command=self.go_back,
        ).pack(pady=15)

        self.load_data()

    def load_data(self):
        """Load all complaints."""
        db = get_session()
        service = ComplaintService(db)
        rows = service.get_all_complaints()
        db.close()

        for r in rows:
            self.table.insert(
                "",
                "end",
                values=(
                    r["complaint_id"],
                    r["tenant_name"],
                    r["apartment_label"],
                    r["status"],
                ),
            )

    def go_back(self):
        """Return to complaints home."""
        from ui.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(lambda parent, mw: ComplaintsHome(parent, mw))