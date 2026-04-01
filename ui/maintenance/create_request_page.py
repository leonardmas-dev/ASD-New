# Student: Ishak Askar    StudentID: 24023614

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from backend.maintenance_service import MaintenanceService
from database.session import get_session
from database.models import Tenant, Lease, Apartment
from sqlalchemy.orm import joinedload


class CreateRequestPage(tk.Frame):
    """Staff creates a maintenance request."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Create Maintenance Request", font=("Arial", 22)).pack(pady=20)

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

        tk.Label(form, text="Priority:").grid(row=3, column=0, sticky="e")
        self.priority_combo = ttk.Combobox(
            form,
            values=["Low", "Medium", "High"],
            state="readonly",
            width=15,
        )
        self.priority_combo.grid(row=3, column=1, padx=5, pady=5, sticky="w")
        self.priority_combo.set("Medium")

        tk.Label(form, text="Status:").grid(row=4, column=0, sticky="e")
        self.status_combo = ttk.Combobox(
            form,
            values=["Pending", "In Progress", "Completed"],
            state="readonly",
            width=15,
        )
        self.status_combo.grid(row=4, column=1, padx=5, pady=5, sticky="w")
        self.status_combo.set("Pending")

        tk.Label(form, text="Scheduled Date (optional):").grid(row=5, column=0, sticky="e")
        self.scheduled_entry = tk.Entry(form, width=25)
        self.scheduled_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")
        self.scheduled_entry.insert(0, "YYYY-MM-DD HH:MM")

        tk.Label(form, text="Time Taken Hours (optional):").grid(row=6, column=0, sticky="e")
        self.time_entry = tk.Entry(form, width=10)
        self.time_entry.grid(row=6, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Cost (optional):").grid(row=7, column=0, sticky="e")
        self.cost_entry = tk.Entry(form, width=10)
        self.cost_entry.grid(row=7, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Notes (optional):").grid(row=8, column=0, sticky="e")
        self.notes_entry = tk.Entry(form, width=45)
        self.notes_entry.grid(row=8, column=1, padx=5, pady=5)

        tk.Label(form, text="Assign Staff:").grid(row=9, column=0, sticky="e")
        self.staff_combo = ttk.Combobox(form, state="readonly", width=35)
        self.staff_combo.grid(row=9, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Create Request", command=self.save, width=18).grid(
            row=0, column=0, padx=5
        )
        tk.Button(btn_frame, text="Back", command=self.go_back, width=10).grid(
            row=0, column=1, padx=5
        )

        self._load_dropdowns()

    def _load_dropdowns(self):
        db = get_session()

        tenants = db.query(Tenant).filter(Tenant.is_active == True).all()

        service = MaintenanceService(db)
        staff = service.get_maintenance_staff()

        db.close()

        self.tenant_map = {
            f"{t.tenant_id} - {t.first_name} {t.last_name}": t.tenant_id for t in tenants
        }
        self.tenant_combo["values"] = list(self.tenant_map.keys())

        self.staff_map = {s["name"]: s["user_id"] for s in staff}
        self.staff_combo["values"] = list(self.staff_map.keys())

    def on_tenant_selected(self, event=None):
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
        desc = self.desc_entry.get().strip()
        if not desc:
            messagebox.showerror("Error", "Enter a description.")
            return

        tenant_label = self.tenant_combo.get()
        staff_label = self.staff_combo.get()
        apartment_label = self.apartment_combo.get()
        priority = self.priority_combo.get()
        status = self.status_combo.get()

        if not tenant_label or not staff_label or not apartment_label:
            messagebox.showerror("Error", "Select tenant, apartment, and staff.")
            return

        tenant_id = self.tenant_map[tenant_label]
        apartment_id = self.apartment_map[apartment_label]
        staff_user_id = self.staff_map[staff_label]

        scheduled_date = None
        raw_date = self.scheduled_entry.get().strip()
        if raw_date and raw_date != "YYYY-MM-DD HH:MM":
            try:
                scheduled_date = datetime.strptime(raw_date, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Invalid scheduled date format.")
                return

        time_taken_hours = None
        if self.time_entry.get().strip():
            try:
                time_taken_hours = float(self.time_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Time taken must be a number.")
                return

        cost = None
        if self.cost_entry.get().strip():
            try:
                cost = float(self.cost_entry.get().strip())
            except ValueError:
                messagebox.showerror("Error", "Cost must be a number.")
                return

        notes = self.notes_entry.get().strip() or None

        db = get_session()
        service = MaintenanceService(db)

        ok = service.create_request(
            tenant_id,
            apartment_id,
            desc,
            priority,
            staff_user_id,
            status,
            scheduled_date,
            time_taken_hours,
            cost,
            notes,
        )

        db.close()

        if ok:
            messagebox.showinfo("Success", "Request created.")
            self.desc_entry.delete(0, tk.END)
            self.notes_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.cost_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to create request.")

    def go_back(self):
        from ui.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(lambda parent, mw: MaintenanceHome(parent, mw))