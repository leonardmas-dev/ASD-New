import tkinter as tk
from tkinter import ttk

from database.session import SessionLocal
from backend.complaint_service import ComplaintService


class ViewComplaintsPage(tk.Frame):
    """
    Displays all complaints submitted by the tenant.
    """

    def __init__(self, parent, main_window):
        super().__init__(parent)

        # Store references
        self.main_window = main_window
        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id

        # --- Header ---
        tk.Label(self, text="My Complaints", font=("Arial", 18, "bold")).pack(pady=20)

        # --- Table Container ---
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10)

        # --- Complaints Table ---
        self.table = ttk.Treeview(
            table_frame,
            columns=("status", "date", "description"),
            show="headings",
            height=15,
        )

        # Column setup
        self.table.heading("status", text="Status")
        self.table.heading("date", text="Date")
        self.table.heading("description", text="Description")

        self.table.column("status", width=120)
        self.table.column("date", width=150)
        self.table.column("description", width=400)

        self.table.pack(fill="both", expand=True)

        # Back navigation
        self.add_back_button()

        # Load data
        self.load_complaints()

    # --- Load complaints from backend ---
    def load_complaints(self):
        for row in self.table.get_children():
            self.table.delete(row)

        db = SessionLocal()
        service = ComplaintService(db)

        try:
            complaints = service.get_complaints_for_tenant(self.tenant_id)
        finally:
            db.close()

        # Insert rows
        for c in complaints:
            self.table.insert(
                "",
                "end",
                values=(c["status"], c["created_at"], c["description"]),
            )

    # --- Back Button ---
    def add_back_button(self):
        from ui.tenant_portal.complaints.complaints_home import ComplaintsHome
        tk.Button(
            self,
            text="Back",
            command=lambda: self.main_window.load_page(ComplaintsHome),
        ).pack(pady=20)