import tkinter as tk
from tkinter import ttk

from backend.complaint_service import ComplaintService
from database.session import get_session


class ComplaintsHome(tk.Frame):
    """Tenant view of their complaints."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session

        tk.Label(self, text="My Complaints", font=("Arial", 22)).pack(pady=20)

        # buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Submit Complaint",
            width=20,
            command=self.open_submit_complaint
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="View Complaint History",
            width=20,
            command=self.open_history
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            self,
            text="Back to Dashboard",
            command=self.go_home
        ).pack(pady=10)

        # table
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

    # load tenant complaints
    def load_complaints(self):
        db = get_session()
        service = ComplaintService(db)
        rows = service.get_complaints_for_tenant(self.session.tenant_id)

        # extract before closing session
        comp_rows = []
        for r in rows:
            comp_rows.append((
                r["description"],
                r["status"],
                r["submitted_at"],
            ))

        db.close()

        for row in comp_rows:
            self.table.insert("", "end", values=row)

    # open submit complaint page
    def open_submit_complaint(self):
        from ui.tenant_portal.complaints.submit_complaint import SubmitComplaintPage
        self.main_window.load_page(SubmitComplaintPage)

    # open complaint history page
    def open_history(self):
        from ui.tenant_portal.complaints.view_complaints import TenantComplaintHistoryPage
        self.main_window.load_page(TenantComplaintHistoryPage)

    # back to dashboard
    def go_home(self):
        from ui.tenant_portal.tenant_dashboard import TenantDashboard
        self.main_window.load_page(TenantDashboard)