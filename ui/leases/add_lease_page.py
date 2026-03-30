import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database.session import SessionLocal
from backend.lease_service import LeaseService


class AddLeasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # main_window

        tk.Label(self, text="Create New Lease Agreement", font=("Arial", 18, "bold")).pack(pady=20)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Tenant ID:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.tenant_entry = tk.Entry(form_frame)
        self.tenant_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Apartment ID:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.apt_entry = tk.Entry(form_frame)
        self.apt_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Monthly Rent (£):").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.rent_entry = tk.Entry(form_frame)
        self.rent_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Deposit Amount (£):").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.deposit_entry = tk.Entry(form_frame)
        self.deposit_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Start Date (YYYY-MM-DD):").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.start_date_entry = tk.Entry(form_frame)
        self.start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.start_date_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(form_frame, text="Lease Period:").grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.duration_cb = ttk.Combobox(form_frame, values=["6", "12", "24"])
        self.duration_cb.set("12")
        self.duration_cb.grid(row=5, column=1, padx=10, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=30)

        submit_btn = tk.Button(
            btn_frame,
            text="Generate Lease",
            bg="blue",
            fg="white",
            width=20,
            command=self.save_lease,
        )
        submit_btn.pack(side="left", padx=10)

        from ui.leases.leases_home import LeasesHome
        back_btn = tk.Button(
            btn_frame,
            text="Back",
            bg="#95a5a6",
            fg="white",
            width=15,
            command=lambda: self.controller.load_page(LeasesHome),
        )
        back_btn.pack(side="left", padx=10)

    def save_lease(self):
        tenant_id = self.tenant_entry.get()
        apt_id = self.apt_entry.get()
        rent = self.rent_entry.get()
        deposit = self.deposit_entry.get()
        start_date = self.start_date_entry.get()
        duration = self.duration_cb.get()

        if not all([tenant_id, apt_id, rent, deposit]):
            messagebox.showerror("Error", "Please fill in all required fields.")
            return

        db = SessionLocal()
        service = LeaseService(db)
        try:
            success = service.create_lease(tenant_id, apt_id, start_date, duration, rent, deposit)
        finally:
            db.close()

        if success:
            messagebox.showinfo("Success", f"Lease created! Apartment {apt_id} status updated to Occupied.")
            self.clear_fields()
            from ui.leases.lease_list_page import LeaseListPage
            self.controller.load_page(LeaseListPage)
        else:
            messagebox.showerror("Database Error", "Failed to save lease. Ensure IDs exist and data is valid.")

    def clear_fields(self):
        self.tenant_entry.delete(0, tk.END)
        self.apt_entry.delete(0, tk.END)
        self.rent_entry.delete(0, tk.END)
        self.deposit_entry.delete(0, tk.END)