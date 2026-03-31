import tkinter as tk
from tkinter import ttk, messagebox

from backend.maintenance_service import MaintenanceService
from database.session import get_session
from database.models import Tenant, Apartment, Lease


class CreateRequestPage(tk.Frame):
    """Staff creates a maintenance request."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Create Maintenance Request", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Tenant:").grid(row=0, column=0, sticky="e")
        self.tenant_combo = ttk.Combobox(form, state="readonly", width=30)
        self.tenant_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Apartment:").grid(row=1, column=0, sticky="e")
        self.apartment_combo = ttk.Combobox(form, state="readonly", width=30)
        self.apartment_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Description:").grid(row=2, column=0, sticky="e")
        self.desc_entry = tk.Entry(form, width=40)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="Priority:").grid(row=3, column=0, sticky="e")
        self.priority_combo = ttk.Combobox(form, values=["Low", "Medium", "High"], state="readonly")
        self.priority_combo.grid(row=3, column=1, padx=5, pady=5)
        self.priority_combo.set("Medium")

        tk.Button(self, text="Create Request", command=self.save).pack(pady=15)

        self._load_dropdowns()

    def _load_dropdowns(self):
        db = get_session()

        tenants = db.query(Tenant).filter(Tenant.is_active == True).all()
        apartments = db.query(Apartment).filter(Apartment.is_active == True).all()

        db.close()

        self.tenant_map = {f"{t.tenant_id} - {t.first_name} {t.last_name}": t.tenant_id for t in tenants}
        self.apartment_map = {
            f"{a.apartment_id} - {a.location.city}": a.apartment_id for a in apartments
        }

        self.tenant_combo["values"] = list(self.tenant_map.keys())
        self.apartment_combo["values"] = list(self.apartment_map.keys())

    def save(self):
        desc = self.desc_entry.get().strip()
        if not desc:
            messagebox.showerror("Error", "Enter a description.")
            return

        try:
            tenant_id = self.tenant_map[self.tenant_combo.get()]
            apartment_id = self.apartment_map[self.apartment_combo.get()]
            priority = self.priority_combo.get()
        except Exception:
            messagebox.showerror("Error", "Invalid selection.")
            return

        db = get_session()

        # ensure tenant has an active lease for that apartment
        lease = (
            db.query(Lease)
            .filter(
                Lease.tenant_id == tenant_id,
                Lease.apartment_id == apartment_id,
                Lease.is_active == True,
            )
            .first()
        )

        if not lease:
            messagebox.showerror("Error", "Tenant has no active lease for this apartment.")
            db.close()
            return

        service = MaintenanceService(db)
        ok = service.create_request(tenant_id, apartment_id, desc, priority)

        db.close()

        if ok:
            messagebox.showinfo("Success", "Request created.")
        else:
            messagebox.showerror("Error", "Failed to create request.")