import tkinter as tk
from tkinter import ttk, messagebox

from backend.maintenance_service import MaintenanceService
from database.session import get_session
from database.models import MaintenanceRequest


class UpdateRequestPage(tk.Frame):
    """Staff updates an existing maintenance request."""

    def __init__(self, parent, main_window, request_id):
        super().__init__(parent)

        self.request_id = request_id

        tk.Label(self, text="Update Maintenance Request", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Status:").grid(row=0, column=0, sticky="e")
        self.status_combo = ttk.Combobox(
            form,
            values=["Pending", "Scheduled", "In Progress", "Completed"],
            state="readonly",
        )
        self.status_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Time Taken (hours):").grid(row=1, column=0, sticky="e")
        self.time_entry = tk.Entry(form)
        self.time_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Cost (£):").grid(row=2, column=0, sticky="e")
        self.cost_entry = tk.Entry(form)
        self.cost_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="Notes:").grid(row=3, column=0, sticky="e")
        self.notes_entry = tk.Entry(form, width=40)
        self.notes_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Button(self, text="Save Changes", command=self.save).pack(pady=15)

        self.load_data()

    def load_data(self):
        db = get_session()
        req = db.query(MaintenanceRequest).filter(
            MaintenanceRequest.maintenance_request_id == self.request_id
        ).first()
        db.close()

        self.status_combo.set(req.status)
        if req.time_taken_hours:
            self.time_entry.insert(0, req.time_taken_hours)
        if req.cost:
            self.cost_entry.insert(0, req.cost)
        if req.notes:
            self.notes_entry.insert(0, req.notes)

    def save(self):
        status = self.status_combo.get()
        time_taken = self.time_entry.get().strip()
        cost = self.cost_entry.get().strip()
        notes = self.notes_entry.get().strip()

        time_taken = float(time_taken) if time_taken else None
        cost = float(cost) if cost else None

        db = get_session()
        service = MaintenanceService(db)
        ok = service.update_request(self.request_id, status, time_taken, cost, notes)
        db.close()

        if ok:
            messagebox.showinfo("Success", "Request updated.")
        else:
            messagebox.showerror("Error", "Failed to update request.")