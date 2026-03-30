import tkinter as tk


class MaintenanceHome(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session  # logged-in user session

        tk.Label(self, text="Maintenance", font=("Arial", 18, "bold")).pack(pady=40)

        # tenant view – submit + track own requests
        if self.session.is_tenant or self.session.role == "Tenant":
            tk.Button(
                self,
                text="Submit Maintenance Request",
                width=25,
                command=self.open_tenant_maintenance,
            ).pack(pady=10)

        # staff view – full maintenance management
        if self.session.role in ["FrontDesk", "Maintenance", "Admin", "Manager"]:
            tk.Button(
                self,
                text="View All Maintenance Requests",
                width=25,
                command=self.open_staff_maintenance_list,
            ).pack(pady=10)

            tk.Button(
                self,
                text="Create Maintenance Request (Staff)",
                width=25,
                command=self.open_staff_create_request,
            ).pack(pady=10)

    def open_tenant_maintenance(self):
        from ui.tenant_portal.tenant_maintenance_page import TenantMaintenance
        self.main_window.load_page(TenantMaintenance)

    def open_staff_maintenance_list(self):
        from ui.maintenance.maintenance_list_page import MaintenanceListPage
        self.main_window.load_page(MaintenanceListPage)

    def open_staff_create_request(self):
        from ui.maintenance.create_request_page import CreateMaintenanceRequestPage
        self.main_window.load_page(CreateMaintenanceRequestPage)