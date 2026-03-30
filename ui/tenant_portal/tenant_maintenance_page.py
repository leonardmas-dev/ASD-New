import tkinter as tk
from tkinter import ttk, messagebox

from database.session import SessionLocal
from database.models import Lease
from backend.maintenance_service import MaintenanceService

from ui.tenant_portal.tenant_dashboard import TenantDashboard


class TenantMaintenance(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id

        self.apartment_id = None
        self.load_active_lease()

        tk.Label(self, text="Maintenance Request", fg="blue", bg="white", font=("Arial", 16, "bold")).pack(pady=10)

        form = tk.Frame(self)
        form.pack(pady=5)

        tk.Label(form, text="Category:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.category_cb = ttk.Combobox(form, values=["Plumbing", "Electrical", "Heating", "General"])
        self.category_cb.set("General")
        self.category_cb.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Priority:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.priority_cb = ttk.Combobox(form, values=["Low", "Medium", "High"])
        self.priority_cb.set("Medium")
        self.priority_cb.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(self, text="Description:").pack(pady=5)
        self.desc_text = tk.Text(self, height=6, width=60)
        self.desc_text.pack(pady=5)

        tk.Button(self, text="Submit Request", command=self.submit_request).pack(pady=10)

        cols = ("Status", "Date", "Category", "Priority", "Description")
        self.requests_table = ttk.Treeview(self, columns=cols, show="headings")
        for c in cols:
            self.requests_table.heading(c, text=c)
        self.requests_table.column("Status", width=100)
        self.requests_table.column("Date", width=150)
        self.requests_table.column("Category", width=120)
        self.requests_table.column("Priority", width=80)
        self.requests_table.column("Description", width=300)
        self.requests_table.pack(pady=10, fill="x")

        tk.Button(self, text="View Requests", command=self.show_requests).pack(pady=5)

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
                self.apartment_id = lease.apartment_id
            else:
                self.apartment_id = None
                messagebox.showwarning("Warning", "No active lease found. Maintenance requests will be disabled.")
        finally:
            db.close()

    def submit_request(self):
        description = self.desc_text.get("1.0", tk.END).strip()
        category = self.category_cb.get()
        priority = self.priority_cb.get()

        if not description:
            messagebox.showwarning("Warning", "Please enter a description.")
            return

        if not self.apartment_id:
            messagebox.showerror("Error", "No active apartment found for this tenant.")
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
            messagebox.showinfo("Submitted", "Maintenance request submitted.")
            self.desc_text.delete("1.0", tk.END)
            self.show_requests()
        else:
            messagebox.showerror("Error", "Failed to submit request.")

    def show_requests(self):
        for row in self.requests_table.get_children():
            self.requests_table.delete(row)

        db = SessionLocal()
        service = MaintenanceService(db)
        try:
            requests = service.get_requests_for_tenant(self.tenant_id)
        finally:
            db.close()

        for r in requests:
            self.requests_table.insert(
                "",
                "end",
                values=(
                    r["status"],
                    r["created_at"],
                    r["category"],
                    r["priority"],
                    r["description"],
                ),
            )