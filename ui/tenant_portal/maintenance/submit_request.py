import tkinter as tk
from tkinter import messagebox

from backend.maintenance_service import MaintenanceService
from database.session import get_session
from database.models import Lease


class SubmitRequest(tk.Frame):
    """Tenant submits a new maintenance request."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.session = main_window.user_session

        tk.Label(self, text="Submit Maintenance Request", font=("Arial", 22)).pack(pady=20)

        tk.Label(self, text="Describe the issue:").pack()
        self.desc_entry = tk.Entry(self, width=60)
        self.desc_entry.pack(pady=5)

        tk.Button(self, text="Submit", command=self.submit).pack(pady=10)

        tk.Button(
            self,
            text="Back",
            command=self.go_back
        ).pack(pady=10)

    def submit(self):
        desc = self.desc_entry.get().strip()
        if not desc:
            messagebox.showerror("Error", "Please enter a description.")
            return

        db = get_session()

        lease = (
            db.query(Lease)
            .filter(
                Lease.tenant_id == self.session.tenant_id,
                Lease.is_active == True
            )
            .first()
        )

        if not lease:
            messagebox.showerror("Error", "No active lease found.")
            db.close()
            return

        service = MaintenanceService(db)

        ok = service.create_request(
            tenant_id=self.session.tenant_id,
            apartment_id=lease.apartment_id,
            description=desc,
            priority="Medium",   # default priority chosen by system, staff can change this later them selves
            staff_user_id=None,  # tenant cannot assign staff to complete that request, staff member will add this manually
        )

        db.close()

        if ok:
            messagebox.showinfo("Success", "Maintenance request submitted.")
            self.desc_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to submit request.")

    def go_back(self):
        from ui.tenant_portal.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(lambda parent, mw: MaintenanceHome(parent, mw))