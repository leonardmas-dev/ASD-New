import tkinter as tk
from tkinter import ttk, messagebox

from backend.complaint_service import ComplaintService
from database.session import get_session
from database.models import Tenant, Lease, Apartment
from sqlalchemy.orm import joinedload


class AddComplaintPage(tk.Frame):
    """Staff creates a complaint."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Add Complaint", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Tenant:").grid(row=0, column=0, sticky="e")
        self.tenant_combo = ttk.Combobox(form, state="readonly", width=35)
        self.tenant_combo.grid(row=0, column=1, padx=5, pady=5)
        self.tenant_combo.bind("<<ComboboxSelected>>", self.on_tenant_selected)

        tk.Label(form, text="Apartment:").grid(row=1, column=0, sticky="e")
        self.apartment_combo = ttk.Combobox(form, state="readonly", width=35)
        self.apartment_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Description:").grid(row=2, column=0, sticky="e")
        self.desc_entry = tk.Entry(form, width=45)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="Create Complaint",
            width=18,
            command=self.save,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Back",
            width=10,
            command=self.go_back,
        ).grid(row=0, column=1, padx=5)

        self._load_tenants()

    def _load_tenants(self):
        """Load active tenants."""
        db = get_session()
        tenants = db.query(Tenant).filter(Tenant.is_active == True).all()
        db.close()

        self.tenant_map = {
            f"{t.tenant_id} - {t.first_name} {t.last_name}": t.tenant_id
            for t in tenants
        }
        self.tenant_combo["values"] = list(self.tenant_map.keys())

    def on_tenant_selected(self, event=None):
        """Auto-fill apartment based on tenant's active lease."""
        label = self.tenant_combo.get()
        if not label:
            return

        tenant_id = self.tenant_map[label]

        db = get_session()
        lease = (
            db.query(Lease)
            .options(joinedload(Lease.apartment).joinedload(Apartment.location))
            .filter(Lease.tenant_id == tenant_id, Lease.is_active == True)
            .first()
        )
        db.close()

        if not lease:
            messagebox.showerror("Error", "This tenant has no active lease.")
            self.apartment_combo.set("")
            return

        apt = lease.apartment
        apt_label = f"{apt.apartment_id} - {apt.location.city} ({apt.apartment_type})"

        self.apartment_map = {apt_label: apt.apartment_id}
        self.apartment_combo["values"] = [apt_label]
        self.apartment_combo.set(apt_label)
        self.apartment_combo.config(state="disabled")

    def save(self):
        """Create complaint."""
        desc = self.desc_entry.get().strip()
        if not desc:
            messagebox.showerror("Error", "Enter a description.")
            return

        tenant_label = self.tenant_combo.get()
        apartment_label = self.apartment_combo.get()

        if not tenant_label or not apartment_label:
            messagebox.showerror("Error", "Select tenant and apartment.")
            return

        tenant_id = self.tenant_map[tenant_label]
        apartment_id = self.apartment_map[apartment_label]

        db = get_session()

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

        service = ComplaintService(db)
        ok = service.create_complaint(tenant_id, apartment_id, desc)
        db.close()

        if ok:
            messagebox.showinfo("Success", "Complaint created.")
            self.desc_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to create complaint.")

    def go_back(self):
        """Return to complaints home."""
        from ui.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(lambda parent, mw: ComplaintsHome(parent, mw))