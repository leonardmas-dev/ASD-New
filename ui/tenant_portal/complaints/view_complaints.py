import tkinter as tk
from tkinter import ttk

from backend.complaint_service import ComplaintService
from database.session import get_session


class ViewComplaints(tk.Frame):
    """Read-only list of tenant complaints."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.session = main_window.user_session

        tk.Label(self, text="My Complaint History", font=("Arial", 22)).pack(pady=20)

        self.table = ttk.Treeview(
            self,
            columns=("desc", "status", "submitted", "response"),
            show="headings",
        )

        self.table.heading("desc", text="Description")
        self.table.heading("status", text="Status")
        self.table.heading("submitted", text="Submitted At")
        self.table.heading("response", text="Staff Response")

        self.table.column("desc", width=250)
        self.table.column("status", width=120)
        self.table.column("submitted", width=150)
        self.table.column("response", width=250)

        self.table.pack(fill="both", expand=True, pady=10)

        tk.Button(
            self,
            text="Back",
            command=self.go_back
        ).pack(pady=20)

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
                values=(
                    r["description"],
                    r["status"],
                    r["submitted_at"],
                    r["staff_response"] or "",
                ),
            )

    def go_back(self):
        from ui.tenant_portal.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(lambda parent, mw: ComplaintsHome(parent, mw))