import tkinter as tk
from tkinter import ttk, messagebox

#from backend.tenant_service import fetch_tenants
from database.models import MaintenanceRequest
from datetime import datetime
from database.session import get_session

from ui.tenant_portal.tenant_dashboard import TenantDashboard

class TenantMaintenance(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window


        tk.Label(self, text="Make a Maintenance Request", fg="green", bg="white").pack()

        # Maintenance Request Box
        self.maintenance_box = tk.Text(self, height=10, width=50)
        self.maintenance_box.pack()

        

        tk.Button(self, text="Submit Maintenance Request", command=self.submit_maintenance).pack(pady=10)

        self.requests_table = ttk.Treeview(self, columns=("Status", "Date", "Description"), show="headings")
        self.requests_table.heading("Status", text="Status")
        self.requests_table.heading("Date", text="Submitted")
        self.requests_table.heading("Description", text="Description")
        self.requests_table.pack(pady=10)

        tk.Button(self, text="View Maintenance Requests", command=self.show_requests).pack(pady=10)

        go_homebtn = tk.Button(self, text="Go Home", command=lambda: self.main_window.load_page(TenantDashboard))
        go_homebtn.pack(pady=10)


    def submit_maintenance(self):

        # maintenance details that was written in box
        maintenance_text = self.maintenance_box.get("1.0", tk.END).strip()

        if not maintenance_text:
            messagebox.showwarning("Warning", "Please enter a maintenance request description.")
            return
        
        
        tenant_id = 1

        # Hard coded for now
        lease_id = 1

        # Adds Request into DB
        with get_session() as session:
            maintenance = MaintenanceRequest(
                tenant_id=tenant_id,
                lease_id=lease_id,
                apartment_id = 1,
                description=maintenance_text,
                priority = "Medium",
                submitted_at=datetime.now(),
                status="Pending"
            )



        
            session.add(maintenance)
            session.commit()

        messagebox.showinfo("Submitted", "Maintenance Request submitted!")
        

        # Once Maintenance Request goes through the text field resets
        self.maintenance_box.delete("1.0", tk.END)

    
    def show_requests(self):
        

        # Clear existing rows
        for row in self.requests_table.get_children():
            self.requests_table.delete(row)


        # Hard Coded for Now replace later
        tenant_id = 1

        with get_session() as session:
            requests = session.query(MaintenanceRequest).filter_by(tenant_id=tenant_id).all()

            for req in requests:
                self.requests_table.insert("", "end", values=(
                    req.status,
                    req.submitted_at.strftime("%Y-%m-%d %H:%M"),
                    req.description
                ))