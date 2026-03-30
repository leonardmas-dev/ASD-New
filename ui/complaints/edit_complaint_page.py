import tkinter as tk
from tkinter import ttk, messagebox

from database.session import SessionLocal
from backend.complaint_service import ComplaintService


class EditComplaintPage(tk.Frame):
    def __init__(
        self,
        parent,
        controller,
        complaint_id=None,
        tenant_name="",
        apt_label="",
        category="",
        status="",
        **kwargs,
    ):
        super().__init__(parent)
        self.controller = controller
        self.complaint_id = complaint_id

        tk.Label(self, text="Update Complaint", font=("Arial", 18, "bold")).pack(pady=20)

        info = tk.LabelFrame(self, text="Complaint Info", padx=20, pady=10)
        info.pack(fill="x", padx=20, pady=10)

        tk.Label(info, text=f"Complaint ID: {complaint_id}").pack(anchor="w")
        tk.Label(info, text=f"Tenant: {tenant_name}").pack(anchor="w")
        tk.Label(info, text=f"Apartment: {apt_label}").pack(anchor="w")
        tk.Label(info, text=f"Category: {category}").pack(anchor="w")

        form = tk.LabelFrame(self, text="Update Details", padx=20, pady=10)
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Status:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.status_cb = ttk.Combobox(form, values=["Open", "Reviewed", "Resolved"])
        self.status_cb.set(status)
        self.status_cb.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Resolution Notes:").grid(row=1, column=0, sticky="ne", padx=10, pady=5)
        self.notes_text = tk.Text(form, width=40, height=5)
        self.notes_text.grid(row=1, column=1, padx=10, pady=5)

        btns = tk.Frame(self)
        btns.pack(pady=20)

        tk.Button(
            btns,
            text="Save Changes",
            bg="#f39c12",
            fg="white",
            width=15,
            command=self.save_changes,
        ).pack(side="left", padx=10)

        from ui.complaints.complaint_list_page import ComplaintListPage
        tk.Button(
            btns,
            text="Back",
            width=12,
            command=lambda: self.controller.load_page(ComplaintListPage),
        ).pack(side="left", padx=10)

    def save_changes(self):
        status = self.status_cb.get()
        notes = self.notes_text.get("1.0", tk.END).strip()

        db = SessionLocal()
        service = ComplaintService(db)
        try:
            ok = service.update_complaint(
                self.complaint_id,
                status,
                notes,
            )
        finally:
            db.close()

        if ok:
            messagebox.showinfo("Success", "Complaint updated.")
            from ui.complaints.complaint_list_page import ComplaintListPage
            self.controller.load_page(ComplaintListPage)
        else:
            messagebox.showerror("Error", "Failed to update complaint.")