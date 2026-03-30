import tkinter as tk
from tkinter import ttk, messagebox

from database.session import SessionLocal
from backend.maintenance_service import MaintenanceService


class UpdateMaintenanceRequestPage(tk.Frame):
    def __init__(
        self,
        parent,
        controller,
        request_id=None,
        tenant_name="",
        apt_label="",
        category="",
        priority="",
        status="",
        **kwargs,
    ):
        super().__init__(parent)
        self.controller = controller
        self.request_id = request_id

        tk.Label(self, text="Update Maintenance Request", font=("Arial", 18, "bold")).pack(pady=20)

        info = tk.LabelFrame(self, text="Request Info", padx=20, pady=10)
        info.pack(fill="x", padx=20, pady=10)

        tk.Label(info, text=f"Request ID: {request_id}").pack(anchor="w")
        tk.Label(info, text=f"Tenant: {tenant_name}").pack(anchor="w")
        tk.Label(info, text=f"Apartment: {apt_label}").pack(anchor="w")
        tk.Label(info, text=f"Category: {category}").pack(anchor="w")
        tk.Label(info, text=f"Priority: {priority}").pack(anchor="w")

        form = tk.LabelFrame(self, text="Update Details", padx=20, pady=10)
        form.pack(fill="x", padx=20, pady=10)

        tk.Label(form, text="Status:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.status_cb = ttk.Combobox(form, values=["Pending", "In Progress", "Completed"])
        self.status_cb.set(status)
        self.status_cb.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form, text="Resolution Notes:").grid(row=1, column=0, sticky="ne", padx=10, pady=5)
        self.notes_text = tk.Text(form, width=40, height=5)
        self.notes_text.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form, text="Time Taken (hours):").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.time_entry = tk.Entry(form)
        self.time_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form, text="Cost (£):").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.cost_entry = tk.Entry(form)
        self.cost_entry.grid(row=3, column=1, padx=10, pady=5)

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

        from ui.maintenance.maintenance_list_page import MaintenanceListPage
        tk.Button(
            btns,
            text="Back",
            width=12,
            command=lambda: self.controller.load_page(MaintenanceListPage),
        ).pack(side="left", padx=10)

    def save_changes(self):
        status = self.status_cb.get()
        notes = self.notes_text.get("1.0", tk.END).strip()
        time_taken = self.time_entry.get()
        cost = self.cost_entry.get()

        try:
            time_taken = float(time_taken) if time_taken else None
            cost = float(cost) if cost else None
        except ValueError:
            messagebox.showerror("Error", "Time and Cost must be numbers.")
            return

        db = SessionLocal()
        service = MaintenanceService(db)
        try:
            ok = service.update_request(
                self.request_id,
                status,
                notes,
                time_taken,
                cost,
            )
        finally:
            db.close()

        if ok:
            messagebox.showinfo("Success", "Request updated.")
            from ui.maintenance.maintenance_list_page import MaintenanceListPage
            self.controller.load_page(MaintenanceListPage)
        else:
            messagebox.showerror("Error", "Failed to update request.")