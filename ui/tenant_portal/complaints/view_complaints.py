import tkinter as tk
from tkinter import ttk

from backend.complaint_service import ComplaintService
from database.session import get_session


class ViewComplaints(tk.Frame):
    """Read‑only list of tenant complaints."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.session = main_window.user_session

        tk.Label(self, text="View Complaints", font=("Arial", 22)).pack(pady=20)

        self.table = ttk.Treeview(
            self,
            columns=("desc", "status", "submitted"),
            show="headings",
        )
        self.table.heading("desc", text="Description")
        self.table.heading("status", text="Status")
        self.table.heading("submitted", text="Submitted At")
        self.table.pack(fill="both", expand=True, pady=10)

        self.load_complaints()

    def load_complaints(self):
        db = get_session()
        service = ComplaintService(db)
        rows = service.get_complaints_for_tenant(self.session.tenant_id)
        db.close()

        for r in rows:
            self.table.insert(
                "",
                "end",
                values=(r["description"], r["status"], r["submitted_at"]),
            )