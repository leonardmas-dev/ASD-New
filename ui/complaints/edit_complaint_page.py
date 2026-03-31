import tkinter as tk
from tkinter import ttk, messagebox

from backend.complaint_service import ComplaintService
from database.session import get_session
from database.models import Complaint


class EditComplaintPage(tk.Frame):
    """Staff updates a complaint."""

    def __init__(self, parent, main_window, complaint_id):
        super().__init__(parent)

        self.complaint_id = complaint_id

        tk.Label(self, text="Edit Complaint", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Status:").grid(row=0, column=0, sticky="e")
        self.status_combo = ttk.Combobox(
            form,
            values=["Pending", "In Review", "Resolved"],
            state="readonly",
        )
        self.status_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Notes:").grid(row=1, column=0, sticky="e")
        self.notes_entry = tk.Entry(form, width=40)
        self.notes_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(self, text="Save Changes", command=self.save).pack(pady=15)

        self.load_data()

    def load_data(self):
        db = get_session()
        c = db.query(Complaint).filter(Complaint.complaint_id == self.complaint_id).first()
        db.close()

        self.status_combo.set(c.status)
        if c.notes:
            self.notes_entry.insert(0, c.notes)

    def save(self):
        status = self.status_combo.get()
        notes = self.notes_entry.get().strip()

        db = get_session()
        service = ComplaintService(db)
        ok = service.update_complaint(self.complaint_id, status, notes)
        db.close()

        if ok:
            messagebox.showinfo("Success", "Complaint updated.")
        else:
            messagebox.showerror("Error", "Failed to update complaint.")