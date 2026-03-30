import tkinter as tk

class MaintenanceHome(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session

        tk.Label(self, text="Maintenance", font=("Arial", 18)).pack(pady=40)
        print("is_tenant:", self.session.is_tenant)
        print("role:", self.session.role)
        print("tenant_id:", self.session.tenant_id)


        # TENANT MAINTENANCE ONLY
        if self.session.is_tenant or self.session.role == "Tenant":
            tk.Button(self, text="Request Tenant Maintenance", command=self.open_tenant_maintenance).pack(pady=10)

    def open_tenant_maintenance(self):
        from ui.tenant_portal.tenant_maintenance_page import TenantMaintenance
        self.main_window.load_page(TenantMaintenance)