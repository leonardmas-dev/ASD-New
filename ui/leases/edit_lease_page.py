import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database.session import SessionLocal
from backend.lease_service import LeaseService


class EditLeasePage(tk.Frame):
    def __init__(
        self,
        parent,
        controller,
        lease_id=None,
        tenant_name="--",
        apt_id=None,
        rent=0.0,
        **kwargs,
    ):
        super().__init__(parent)
        self.controller = controller

        self.current_lease_id = lease_id
        self.current_apt_id = apt_id

        try:
            self.current_rent = float(str(rent).replace('£', '').replace(',', ''))
        except ValueError:
            self.current_rent = 0.0

        tk.Label(self, text="Manage / Terminate Lease", font=("Arial", 18, "bold")).pack(pady=20)

        info_frame = tk.LabelFrame(self, text="Current Lease Details", padx=20, pady=10)
        info_frame.pack(pady=10, fill="x", padx=30)

        self.lbl_id = tk.Label(info_frame, text=f"Lease ID: {lease_id if lease_id else '--'}")
        self.lbl_id.pack(anchor="w")

        self.lbl_tenant = tk.Label(info_frame, text=f"Tenant: {tenant_name}")
        self.lbl_tenant.pack(anchor="w")

        self.lbl_rent = tk.Label(info_frame, text=f"Monthly Rent: £{self.current_rent:.2f}")
        self.lbl_rent.pack(anchor="w")

        term_frame = tk.LabelFrame(self, text="Early Termination Request", padx=20, pady=10, fg="red")
        term_frame.pack(pady=20, fill="x", padx=30)

        tk.Label(term_frame, text="Notice Date (Today):").grid(row=0, column=0, sticky="w")
        tk.Label(term_frame, text=datetime.now().strftime('%Y-%m-%d')).grid(row=0, column=1, padx=10)

        tk.Label(term_frame, text="Intended Move-out Date:").grid(row=1, column=0, sticky="w")
        self.move_out_entry = tk.Entry(term_frame)
        self.move_out_entry.insert(0, (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'))
        self.move_out_entry.grid(row=1, column=1, padx=10, pady=5)

        calc_btn = tk.Button(term_frame, text="Calculate Penalty (5%)", command=self.calculate_early_exit)
        calc_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.penalty_lbl = tk.Label(term_frame, text="Penalty Due: £0.00", font=("Arial", 10, "bold"))
        self.penalty_lbl.grid(row=3, column=0, columnspan=2)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(
            btn_frame,
            text="Confirm Termination",
            bg="#e74c3c",
            fg="white",
            width=20,
            command=self.confirm_termination,
        ).pack(side="left", padx=10)

        from ui.leases.lease_list_page import LeaseListPage
        tk.Button(
            btn_frame,
            text="Cancel",
            command=lambda: self.controller.load_page(LeaseListPage),
        ).pack(side="left")

    def calculate_early_exit(self):
        # 5% of monthly rent
        penalty = self.current_rent * 0.05
        self.penalty_lbl.config(text=f"Penalty Due: £{penalty:.2f}")
        messagebox.showinfo("Policy Check", "Paragon Policy: 1 month notice is required. 5% penalty applied.")

    def confirm_termination(self):
        if not self.current_lease_id:
            return

        ans = messagebox.askyesno(
            "Confirm",
            "Finalize early termination? This will make the apartment available immediately.",
        )
        if not ans:
            return

        db = SessionLocal()
        service = LeaseService(db)
        try:
            penalty = service.terminate_lease(self.current_lease_id, self.current_apt_id)
        finally:
            db.close()

        if penalty is not None:
            messagebox.showinfo("Success", f"Lease terminated.\nPenalty of £{penalty:.2f} recorded.")
            from ui.leases.lease_list_page import LeaseListPage
            self.controller.load_page(LeaseListPage)
        else:
            messagebox.showerror("Error", "Could not process termination.")