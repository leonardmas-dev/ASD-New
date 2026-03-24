import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class EditLeasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Manage / Terminate Lease", font=("Arial", 18, "bold")).pack(pady=20)

        # Info Section (Displaying current lease details)
        info_frame = tk.LabelFrame(self, text="Current Lease Details", padx=20, pady=10)
        info_frame.pack(pady=10, fill="x", padx=30)

        self.lbl_tenant = tk.Label(info_frame, text="Tenant: [Name/NI]")
        self.lbl_tenant.pack(anchor="w")
        
        self.lbl_apt = tk.Label(info_frame, text="Apartment: [Apt ID]")
        self.lbl_apt.pack(anchor="w")

        self.lbl_rent = tk.Label(info_frame, text="Monthly Rent: £1200") # Example
        self.lbl_rent.pack(anchor="w")

        # --- Early Termination Section ---
        term_frame = tk.LabelFrame(self, text="Early Termination Request", padx=20, pady=10, fg="red")
        term_frame.pack(pady=20, fill="x", padx=30)

        tk.Label(term_frame, text="Notice Date (Today):").grid(row=0, column=0, sticky="w")
        self.notice_date_lbl = tk.Label(term_frame, text=datetime.now().strftime('%Y-%m-%d'))
        self.notice_date_lbl.grid(row=0, column=1, padx=10)

        tk.Label(term_frame, text="Intended Move-out Date:").grid(row=1, column=0, sticky="w")
        self.move_out_entry = tk.Entry(term_frame)
        self.move_out_entry.insert(0, (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d'))
        self.move_out_entry.grid(row=1, column=1, padx=10, pady=5)

        # Button to calculate penalty
        calc_btn = tk.Button(term_frame, text="Calculate Penalty", command=self.calculate_early_exit)
        calc_btn.grid(row=2, column=0, columnspan=2, pady=10)

        self.penalty_lbl = tk.Label(term_frame, text="Penalty Due: £0.00", font=("Arial", 10, "bold"))
        self.penalty_lbl.grid(row=3, column=0, columnspan=2)

        # Final Confirmation
        confirm_btn = tk.Button(self, text="Confirm Termination", bg="red", fg="white", 
                                 command=self.confirm_termination)
        confirm_btn.pack(pady=20)

    def calculate_early_exit(self):
        # Business Logic: 5% of monthly rent
        # In real code, you'd pull this rent value from the DB
        rent = 1200 
        penalty = rent * 0.05
        self.penalty_lbl.config(text=f"Penalty Due: £{penalty:.2f}")
        messagebox.showinfo("Notice Period", "Note: 1 month notice is required as per Paragon policy.")

    def confirm_termination(self):
        # 1. Check if 1 month notice is given
        # 2. Apply 5% penalty to the billing table
        # 3. Mark Lease as 'Terminated'
        # 4. Mark Apartment as 'Available'
        messagebox.showinfo("Success", "Lease terminated. Apartment status updated to 'Available'.")
        self.controller.show_frame("LeaseListPage")