import tkinter as tk
from tkinter import ttk, messagebox

#from backend.tenant_service import fetch_tenants
from database.models import Complaint, Lease
from datetime import datetime
from database.session import get_session


from ui.tenant_portal.tenant_dashboard import TenantDashboard

class TenantComplaint(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id
        self.load_leases()


        tk.Label(self, text="Make a Complaint", fg="red", bg="white").pack()

        # Complaint Description Box
        self.complaint_box = tk.Text(self, height=10, width=50)
        self.complaint_box.pack()

        tk.Button(self, text="Submit Complaint", command=self.submit_complaint).pack(pady=10)

        self.complaints_table = ttk.Treeview(self,columns=("Status","Date","Description"), show="headings")
        self.complaints_table.heading("Status", text="Status")
        self.complaints_table.heading("Date", text="Submitted on")
        self.complaints_table.heading("Description", text="Description")
        self.complaints_table.pack(pady=10)

        tk.Button(self,text="View Complaints", command=self.show_complaints).pack(pady=10)

        

        go_homebtn = tk.Button(self, text="Go Home", command=lambda: self.main_window.load_page(TenantDashboard))
        go_homebtn.pack(pady=10)

    def load_leases(self):
        with get_session() as session:
            lease = session.query(Lease).filter_by(
                tenant_id = self.tenant_id,
                is_active = True
            ).first()

            if lease:
                self.lease_id = lease.lease_id
            else:
                self.lease_id = None
                messagebox.showwarning("Warning", "No Active Leases Found")
        
    def submit_complaint(self):

        # Complaint that was written in box
        complaint_text = self.complaint_box.get("1.0", tk.END).strip()

        if not complaint_text:
            messagebox.showwarning("Waning", "Please enter a complaint description.")
            return
        
        
      

        # Adds complaint into DB
        with get_session() as session:
            complaint = Complaint(
                tenant_id=self.tenant_id,
                lease_id=self.lease_id,
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

    def show_complaints(self):
        for row in self.complaints_table.get_children():
            self.complaint_table.delete(row)

        with get_session() as session:
            complaints = session.query(Complaint).filter_by(tenant_id=self.tenant_id).all()
            for c in complaints:
                self.complaints_table.insert("", "end", values=(
                    c.status,
                    c.submitted_at.strftime("%Y-%m-%d %H:%M"),
                    c.description
                ))

    

        

        