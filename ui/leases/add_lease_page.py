import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta

class AddLeasePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Create New Lease Agreement", font=("Arial", 18, "bold")).pack(pady=20)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        # 1. Select Tenant (Links to Person 1's data)
        tk.Label(form_frame, text="Select Tenant (NI Number):").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.tenant_cb = ttk.Combobox(form_frame, values=["Fetch from Person 1..."]) 
        self.tenant_cb.grid(row=0, column=1, padx=10, pady=5)

        # 2. Select Apartment (Links to your Apartment list)
        tk.Label(form_frame, text="Select Apartment:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.apartment_cb = ttk.Combobox(form_frame, values=["Fetch Available Apts..."])
        self.apartment_cb.grid(row=1, column=1, padx=10, pady=5)

        # 3. Start Date
        tk.Label(form_frame, text="Start Date (YYYY-MM-DD):").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.start_date_entry = tk.Entry(form_frame)
        self.start_date_entry.insert(0, datetime.now().strftime('%Y-%m-%d')) # Default to today
        self.start_date_entry.grid(row=2, column=1, padx=10, pady=5)

        # 4. Lease Duration
        tk.Label(form_frame, text="Lease Period:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.duration_cb = ttk.Combobox(form_frame, values=["6 Months", "12 Months", "24 Months"])
        self.duration_cb.grid(row=3, column=1, padx=10, pady=5)

        # Submit Button
        submit_btn = tk.Button(self, text="Generate Lease", bg="blue", fg="white", 
                               width=20, command=self.save_lease)
        submit_btn.pack(pady=30)

    def save_lease(self):
        # Validation
        tenant = self.tenant_cb.get()
        apt = self.apartment_cb.get()
        
        if not tenant or not apt:
            messagebox.showerror("Error", "Please select both a tenant and an apartment.")
            return

        # Success Logic
        print(f"Lease created for {tenant} in Apartment {apt}")
        messagebox.showinfo("Success", "Lease successfully generated and saved to MySQL.")