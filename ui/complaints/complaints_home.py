import tkinter as tk
from tkinter import ttk

from backend.complaint_service import ComplaintService
from database.session import get_session


class ComplaintsHome(tk.Frame):
    """Staff overview of all complaints."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Complaints", font=("Arial", 22)).pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Complaint",
            width=18,
            command=self.open_add_page
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Edit Complaint",
            width=18,
            command=self.open_edit_page
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="View Complaint List",
            width=18,
            command=self.open_list_page
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            btn_frame,
            text="Refresh",
            width=12,
            command=self.refresh_table
        ).grid(row=0, column=3, padx=5)

        self.table = ttk.Treeview(
            self,
            columns=("tenant", "apartment", "desc", "status", "submitted"),
            show="headings",
        )

        for col, text in [
            ("tenant", "Tenant"),
            ("apartment", "Apartment"),
            ("desc", "Description"),
            ("status", "Status"),
            ("submitted", "Submitted At"),
        ]:
            self.table.heading(col, text=text)

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

    def load_data(self):
        db = get_session()
        service = ComplaintService(db)
        rows = service.get_all_complaints()

        extracted = [
            (
                r["tenant_name"],
                r["apartment_label"],
                r["description"],
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

    def open_add_page(self):
        from ui.complaints.add_complaint_page import AddComplaintPage
        self.main_window.load_page(AddComplaintPage)

    def open_edit_page(self):
        from ui.complaints.edit_complaint_page import EditComplaintPage
        self.main_window.load_page(EditComplaintPage)

    def open_list_page(self):
        from ui.complaints.complaint_list_page import ComplaintListPage
        self.main_window.load_page(ComplaintListPage)