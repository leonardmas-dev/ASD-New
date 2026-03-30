import tkinter as tk
from tkinter import messagebox

from database.session import SessionLocal
from database.models import Lease
from backend.complaint_service import ComplaintService


class SubmitComplaintPage(tk.Frame):
    """
    Page for submitting a new complaint.
    Handles lease lookup and complaint creation.
    """

    def __init__(self, parent, main_window):
        super().__init__(parent)

        # Store references
        self.main_window = main_window
        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id

        # Resolve active lease (required for complaint creation)
        self.apartment_id = self.get_active_apartment_id()

        # --- Header ---
        tk.Label(self, text="Submit a Complaint", font=("Arial", 18, "bold")).pack(pady=20)

        # Disable form if no active lease
        if not self.apartment_id:
            tk.Label(self, text="No active lease found. You cannot submit complaints.").pack(pady=10)
            self.add_back_button()
            return

        # --- Complaint Text Box ---
        tk.Label(self, text="Describe your complaint:").pack(pady=5)
        self.text_box = tk.Text(self, height=8, width=60)
        self.text_box.pack(pady=5)

        # --- Submit Button ---
        tk.Button(self, text="Submit Complaint", command=self.submit_complaint).pack(pady=10)

        # Back navigation
        self.add_back_button()

    # --- Helper: Fetch active lease apartment ID ---
    def get_active_apartment_id(self):
        db = SessionLocal()
        try:
            lease = (
                db.query(Lease)
                .filter(Lease.tenant_id == self.tenant_id, Lease.is_active == True)
                .first()
            )
            return lease.apartment_id if lease else None
        finally:
            db.close()

    # --- Submit Handler ---
    def submit_complaint(self):
        description = self.text_box.get("1.0", tk.END).strip()

        if not description:
            messagebox.showwarning("Warning", "Please enter a complaint description.")
            return

        db = SessionLocal()
        service = ComplaintService(db)

        try:
            ok = service.create_complaint(
                tenant_id=self.tenant_id,
                apartment_id=self.apartment_id,
                category="General",
                description=description,
                created_by_staff=False,
            )
        finally:
            db.close()

        if ok:
            messagebox.showinfo("Success", "Complaint submitted successfully.")
            self.text_box.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Failed to submit complaint.")

    # --- Back Button ---
    def add_back_button(self):
        from ui.tenant_portal.complaints.complaints_home import ComplaintsHome
        tk.Button(
            self,
            text="Back",
            command=lambda: self.main_window.load_page(ComplaintsHome),
        ).pack(pady=20)