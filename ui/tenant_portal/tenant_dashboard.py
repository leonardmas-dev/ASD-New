import tkinter as tk

class TenantDashboard(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        tk.Label(self, text="Tenant Dashboard", font=("Arial", 18, "bold")).pack(pady=20)
        tk.Label(self, text="Welcome to your tenant portal.").pack(pady=10)

        tk.Button(self, text="Make a Complaint", command=self.open_tenant_complaint).pack(pady=10)

        tk.Button(self, text="Maintenance Requests", command=self.open_maintenance_page).pack(pady=10)

        tk.Button(self, text="Payments", command=self.open_payments).pack(pady=10)

    def open_tenant_complaint(self):
        from ui.tenant_portal.tenant_complaints_page import TenantComplaint
        self.main_window.load_page(TenantComplaint)

    def open_maintenance_page(self):
        from ui.tenant_portal.tenant_maintenance_page import TenantMaintenance
        self.main_window.load_page(TenantMaintenance)
        
    def open_payments(self):
        from ui.tenant_portal.tenant_payments_page import TenantPayment
        self.main_window.load_page(TenantPayment)