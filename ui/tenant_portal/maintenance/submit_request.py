import tkinter as tk
from tkinter import ttk, messagebox

from database.session import SessionLocal
from database.models import Lease
from backend.maintenance_service import MaintenanceService


class SubmitMaintenanceRequestPage(tk.Frame):
    """
    Page for submitting a new maintenance request.
    Handles lease lookup and request creation.
    """

    def __init__(self, parent, main_window):
        super().__init__(parent)

        # Store references
        self.main_window = main_window
        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id

        # Resolve active lease
        self.apartment_id = self.get_active_apartment_id()

        # --- Header ---
        tk.Label(self, text="Submit Maintenance Request", font=("Arial", 18, "bold")).pack(pady=20)

        # Disable form if no active lease
        if not self.apartment_id:
            tk.Label(self, text="No active lease found. You cannot submit maintenance requests.").pack(pady=10)
            self.add_back_button()
            return

        # --- Form Container ---
        form = tk.Frame(self)
        form.pack(pady=10)

        # Category dropdown
        tk.Label(form, text="Category:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.category_cb = ttk.Combobox(form, values=["Plumbing", "Electrical", "Heating", "General"])
        self.category_cb.set("General")
        self.category_cb.grid(row=0, column=1, padx=5, pady=5)

        # Priority dropdown
        tk.Label(form, text="Priority:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.priority_cb = ttk.Combobox(form, values=["Low", "Medium", "High"])
        self.priority_cb.set("Medium")
        self.priority_cb.grid(row=1, column=1, padx=5, pady=5)

        # Description box
        tk.Label(self, text="Description:").pack(pady=5)
        self.desc_text = tk.Text(self, height=6, width=60)
        self.desc_text.pack(pady=5)

        # Submit button
        tk.Button(self, text="Submit Request", command=self.submit_request).pack(pady=10)

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
    def submit_request(self):
        description = self.desc_text.get("1.0", tk.END).strip()
        category = self.category_cb.get()
        priority = self.priority_cb.get()

        if not description:
            messagebox.showwarning("Warning", "Please enter a description.")
            return

        db = SessionLocal()
        service = MaintenanceService(db)

        try:
            ok = service.create_request(
                tenant_id=self.tenant_id,
                apartment_id=self.apartment_id,
                category=category,
                description=description,
                priority=priority,
                created_by_staff=False,
            )
        finally:
            db.close()

        if ok:
            messagebox.showinfo("Success", "Maintenance request submitted.")
            self.desc_text.delete("1.0", tk.END)
        else:
            messagebox.showerror("Error", "Failed to submit request.")

    # --- Back Button ---
    def add_back_button(self):
        from ui.tenant_portal.maintenance.maintenance_home import MaintenanceHome
        tk.Button(
            self,
            text="Back",
            command=lambda: self.main_window.load_page(MaintenanceHome),
        ).pack(pady=20)