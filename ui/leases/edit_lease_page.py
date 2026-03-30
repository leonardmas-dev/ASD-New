import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import sys
import os

# Ensure backend can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from backend.lease_service import terminate_lease

class EditLeasePage(tk.Frame):
    # 1. UPDATED: Catching data passed from the List Page via kwargs
    def __init__(self, parent, controller, lease_id=None, tenant_name="--", apt_id=None, rent=0.0, **kwargs):
        super().__init__(parent)
        self.controller = controller
        
        # Store passed data
        self.current_lease_id = lease_id
        self.current_apt_id = apt_id
        # Clean the rent string if it has a £ symbol
        try:
            self.current_rent = float(str(rent).replace('£', '').replace(',', ''))
        except ValueError:
            self.current_rent = 0.0

        tk.Label(self, text="Manage / Terminate Lease", font=("Arial", 18, "bold")).pack(pady=20)

        # --- Info Section ---
        info_frame = tk.LabelFrame(self, text="Current Lease Details", padx=20, pady=10)
        info_frame.pack(pady=10, fill="x", padx=30)

        self.lbl_id = tk.Label(info_frame, text=f"Lease ID: {lease_id if lease_id else '--'}")
        self.lbl_id.pack(anchor="w")

        self.lbl_tenant = tk.Label(info_frame, text=f"Tenant: {tenant_name}")
        self.lbl_tenant.pack(anchor="w")
        
        self.lbl_rent = tk.Label(info_frame, text=f"Monthly Rent: £{self.current_rent:.2f}")
        self.lbl_rent.pack(anchor="w")

        # --- Early Termination Section ---
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

        # --- Action Buttons ---
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Confirm Termination", bg="#e74c3c", fg="white", 
                  width=20, command=self.confirm_termination).pack(side="left", padx=10)
        
        # 2. UPDATED: Back/Cancel logic using load_page
        from ui.leases.lease_list_page import LeaseListPage
        tk.Button(btn_frame, text="Cancel", 
                  command=lambda: self.controller.load_page(LeaseListPage)).pack(side="left")

    def calculate_early_exit(self):
        # Calculation: 5% of monthly rent
        penalty = self.current_rent * 0.05
        self.penalty_lbl.config(text=f"Penalty Due: £{penalty:.2f}")
        messagebox.showinfo("Policy Check", "Paragon Policy: 1 month notice is required. 5% penalty applied.")

    def confirm_termination(self):
        if not self.current_lease_id: return
        
        ans = messagebox.askyesno("Confirm", "Finalize early termination? This will make the apartment available immediately.")
        if ans:
            penalty = terminate_lease(self.current_lease_id, self.current_apt_id)
            if penalty is not None:
                messagebox.showinfo("Success", f"Lease terminated.\nPenalty of £{penalty:.2f} recorded.")
                # 3. UPDATED: Redirect back to list
                from ui.leases.lease_list_page import LeaseListPage
                self.controller.load_page(LeaseListPage)