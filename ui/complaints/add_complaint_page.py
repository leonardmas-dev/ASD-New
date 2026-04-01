import tkinter as tk
from tkinter import ttk, messagebox

from backend.complaint_service import ComplaintService
from database.session import get_session
from database.models import Tenant, Apartment, Lease


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

        tk.Label(form, text="Apartment:").grid(row=1, column=0, sticky="e")
        self.apartment_combo = ttk.Combobox(form, state="readonly", width=35)
        self.apartment_combo.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Description:").grid(row=2, column=0, sticky="e")
        self.desc_entry = tk.Entry(form, width=45)
        self.desc_entry.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Create Complaint", width=18, command=self.save).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", width=10, command=self.go_back).grid(row=0, column=1, padx=5)

        self._load_dropdowns()

    def _load_dropdowns(self):
        db = get_session()

        tenants = db.query(Tenant).filter(Tenant.is_active == True).all()
        apartments = db.query(Apartment).filter(Apartment.is_active == True).all()

        db.close()

        self.tenant_map = {
            f"{t.tenant_id} - {t.first_name} {t.last_name}": t.tenant_id
            for t in tenants
        }

        self.apartment_map = {
            f"{a.apartment_id} - {a.location.city} ({a.apartment_type})": a.apartment_id
            for a in apartments
        }

        self.tenant_combo["values"] = list(self.tenant_map.keys())
        self.apartment_combo["values"] = list(self.apartment_map.keys())

    def save(self):
        desc = self.desc_entry.get().strip()
        if not desc:
            messagebox.showerror("Error", "Enter a description.")
            return

        tenant_label = self.tenant_combo.get()
        apartment_label = self.apartment_combo.get()

        if not tenant_label or not apartment_label:
            messagebox.showerror("Error", "Select tenant and apartment.")
            return

        tenant_id = self.tenant_map.get(tenant_label)
        apartment_id = self.apartment_map.get(apartment_label)

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
        from ui.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(ComplaintsHome)