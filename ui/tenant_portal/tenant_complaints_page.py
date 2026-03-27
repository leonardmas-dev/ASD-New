import tkinter as tk
from tkinter import ttk, messagebox

#from backend.tenant_service import fetch_tenants
from database.models import Complaint
from datetime import datetime
from database.session import get_session

from ui.tenant_portal.tenant_dashboard import TenantDashboard

class TenantComplaint(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window


        tk.Label(self, text="Make a Complaint", fg="red", bg="white").pack()

        # Complaint Description Box
        self.complaint_box = tk.Text(self, height=10, width=50)
        self.complaint_box.pack()

        tk.Button(self, text="Submit Complaint", command=self.submit_complaint).pack(pady=10)

        

        

        go_homebtn = tk.Button(self, text="Go Home", command=lambda: self.main_window.load_page(TenantDashboard))
        go_homebtn.pack(pady=10)
        
    def submit_complaint(self):

        # Complaint that was written in box
        complaint_text = self.complaint_box.get("1.0", tk.END).strip()

        if not complaint_text:
            messagebox.showwarning("Warning", "Please enter a complaint description.")
            return
        
        
        tenant_id = 1

        # Hard coded for now
        lease_id = 1

        # Adds complaint into DB
        with get_session() as session:
            complaint = Complaint(
                tenant_id=tenant_id,
                lease_id=lease_id,
                description=complaint_text,
                status="Pending",
                submitted_at=datetime.now()
                
            )
            session.add(complaint)
            session.commit()

        messagebox.showinfo("Submitted", "Complaint submitted!")
        #messagebox.askyesno

        # Once Complaint goes through the text field resets
        self.complaint_box.delete("1.0", tk.END)

    

        

        