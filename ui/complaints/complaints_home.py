import tkinter as tk


class ComplaintsHome(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session

        tk.Label(self, text="Complaints", font=("Arial", 18, "bold")).pack(pady=40)

        # tenant view – submit + view own complaints
        if self.session.is_tenant or self.session.role == "Tenant":
            tk.Button(
                self,
                text="Submit a Complaint",
                width=25,
                command=self.open_tenant_complaint,
            ).pack(pady=10)

        # staff view – full complaint management
        if self.session.role in ["FrontDesk", "Admin", "Manager"]:
            tk.Button(
                self,
                text="View All Complaints",
                width=25,
                command=self.open_staff_complaint_list,
            ).pack(pady=10)

            tk.Button(
                self,
                text="Create Complaint (Staff)",
                width=25,
                command=self.open_staff_add_complaint,
            ).pack(pady=10)

    def open_tenant_complaint(self):
        from ui.tenant_portal.tenant_complaints_page import TenantComplaint
        self.main_window.load_page(TenantComplaint)

    def open_staff_complaint_list(self):
        from ui.complaints.complaint_list_page import ComplaintListPage
        self.main_window.load_page(ComplaintListPage)

    def open_staff_add_complaint(self):
        from ui.complaints.add_complaint_page import AddComplaintPage
        self.main_window.load_page(AddComplaintPage)