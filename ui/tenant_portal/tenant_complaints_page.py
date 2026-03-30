import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from database.session import SessionLocal
from database.models import Lease
from backend.complaint_service import ComplaintService

from ui.tenant_portal.tenant_dashboard import TenantDashboard


class TenantComplaint(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id

        self.apartment_id = None
        self.load_active_lease()

        tk.Label(self, text="Make a Complaint", fg="red", bg="white", font=("Arial", 16, "bold")).pack(pady=10)

        self.complaint_box = tk.Text(self, height=8, width=60)
        self.complaint_box.pack(pady=5)

        tk.Button(self, text="Submit Complaint", command=self.submit_complaint).pack(pady=10)

        cols = ("Status", "Date", "Description")
        self.complaints_table = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.complaints_table.heading(c, text=c)
        self.complaints_table.column("Status", width=100)
        self.complaints_table.column("Date", width=150)
        self.complaints_table.column("Description", width=350)
        self.complaints_table.pack(pady=10, fill="x")

        tk.Button(self, text="View Complaints", command=self.show_complaints).pack(pady=5)

        tk.Button(
            self,
            text="Go Home",
            command=lambda: self.main_window.load_page(TenantDashboard),
        ).pack(pady=10)

    def load_active_lease(self):
        db = SessionLocal()
        try:
            lease = (
                db.query(Lease)
                .filter(Lease.tenant_id == self.tenant_id, Lease.is_active == True)
                .first()
            )
            if lease:
                # assume lease has apartment_id
                self.apartment_id = lease.apartment_id
            else:
                self.apartment_id = None
                messagebox.showwarning("Warning", "No active lease found. Complaints will be disabled.")
        finally:
            db.close()

    def submit_complaint(self):
        complaint_text = self.complaint_box.get("1.0", tk.END).strip()

        if not complaint_text:
            messagebox.showwarning("Warning", "Please enter a complaint description.")
            return

        if not self.apartment_id:
            messagebox.showerror("Error", "No active apartment found for this tenant.")
            return

        db = SessionLocal()
        service = ComplaintService(db)
        try:
            ok = service.create_complaint(
                tenant_id=self.tenant_id,
                apartment_id=self.apartment_id,
                category="General",
                description=complaint_text,
                created_by_staff=False,
            )
        finally:
            db.close()

        if ok:
            messagebox.showinfo("Submitted", "Complaint submitted.")
            self.complaint_box.delete("1.0", tk.END)
            self.show_complaints()
        else:
            messagebox.showerror("Error", "Failed to submit complaint.")

    def show_complaints(self):
        for row in self.complaints_table.get_children():
            self.complaints_table.delete(row)

        db = SessionLocal()
        service = ComplaintService(db)
        try:
            complaints = service.get_complaints_for_tenant(self.tenant_id)
        finally:
            db.close()

        for c in complaints:
            self.complaints_table.insert(
                "",
                "end",
                values=(
                    c["status"],
                    c["created_at"],
                    c["description"],
                ),
            )