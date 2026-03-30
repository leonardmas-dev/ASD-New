import tkinter as tk

class ComplaintsHome(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        # Logged-in user session
        self.session = main_window.user_session
        tk.Label(self, text="Complaints", font=("Arial", 18)).pack(pady=40)


        # TENANT RELATED COMPLAINTS ONLY
        if self.session.is_tenant or self.session.role == "Tenant":

            tk.Button(self, text="Make a Tenant related complaint", command=self.open_tenant_complaint).pack(pady=10)

    def open_tenant_complaint(self):
        from ui.tenant_portal.tenant_complaints_page import TenantComplaint
        self.main_window.load_page(TenantComplaint)