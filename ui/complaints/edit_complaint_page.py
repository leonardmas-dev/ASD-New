import tkinter as tk
from tkinter import ttk, messagebox

from backend.complaint_service import ComplaintService
from database.session import get_session


class EditComplaintPage(tk.Frame):
    """Staff updates an existing complaint."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.current_complaint_id = None

        tk.Label(self, text="Edit Complaint", font=("Arial", 22)).pack(pady=20)

        # complaint selector
        select_frame = tk.Frame(self)
        select_frame.pack(pady=5)

        tk.Label(select_frame, text="Select Complaint:").grid(row=0, column=0, sticky="e")
        self.complaint_combo = ttk.Combobox(select_frame, state="readonly", width=55)
        self.complaint_combo.grid(row=0, column=1, padx=5, pady=5)
        self.complaint_combo.bind("<<ComboboxSelected>>", self.on_select)

        # form fields
        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Status:").grid(row=0, column=0, sticky="e")
        self.status_combo = ttk.Combobox(
            form,
            values=["Pending", "In Review", "Resolved"],
            state="readonly",
            width=20,
        )
        self.status_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Notes:").grid(row=1, column=0, sticky="e")
        self.notes_entry = tk.Entry(form, width=45)
        self.notes_entry.grid(row=1, column=1, padx=5, pady=5)

        # buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="Save Changes",
            width=18,
            command=self.save,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Back",
            width=10,
            command=self.go_back,
        ).grid(row=0, column=1, padx=5)

        self._load_complaints()

    def _load_complaints(self):
        """Load all complaints."""
        db = get_session()
        service = ComplaintService(db)
        rows = service.get_all_complaints()
        db.close()

        self.complaint_map = {
            f"{r['complaint_id']} - {r['tenant_name']} - {r['apartment_label']} ({r['status']})":
                r["complaint_id"]
            for r in rows
        }

        self.complaint_combo["values"] = list(self.complaint_map.keys())

    def on_select(self, event=None):
        """Load selected complaint details."""
        label = self.complaint_combo.get()
        if not label:
            return

        self.current_complaint_id = self.complaint_map.get(label)
        if not self.current_complaint_id:
            return

        db = get_session()
        service = ComplaintService(db)
        comp = service.get_complaint_by_id(self.current_complaint_id)
        db.close()

        if not comp:
            messagebox.showerror("Error", "Complaint not found.")
            return

        self.status_combo.set(comp.get("status", ""))

        self.notes_entry.delete(0, tk.END)
        if comp.get("notes"):
            self.notes_entry.insert(0, comp["notes"])

    def save(self):
        """Save updated complaint details."""
        if not self.current_complaint_id:
            messagebox.showerror("Error", "Select a complaint first.")
            return

        status = self.status_combo.get()
        notes = self.notes_entry.get().strip()

        db = get_session()
        service = ComplaintService(db)
        ok = service.update_complaint(self.current_complaint_id, status, notes)
        db.close()

        if ok:
            messagebox.showinfo("Success", "Complaint updated.")
        else:
            messagebox.showerror("Error", "Failed to update complaint.")

    def go_back(self):
        """Return to complaints home."""
        from ui.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(lambda parent, mw: ComplaintsHome(parent, mw))