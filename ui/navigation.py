import tkinter as tk

class Navigation:
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window

        # Logged-in user session
        self.session = main_window.user_session

        # Build menu based on role
        self.build_menu()

    def build_menu(self):

        # STAFF MENUS

        staff_menus = {
            "Admin": [
                ("Home", self.load_home),
                ("Tenants", self.load_tenants),
                ("Apartments", self.load_apartments),
                ("Leases", self.load_leases),
                ("Payments", self.load_payments),
                ("Maintenance", self.load_maintenance_staff),
                ("Complaints", self.load_complaints_staff),
                ("Reports", self.load_reports),
                ("User Management", self.load_users),
                ("Logout", self.logout),
            ],

            "FrontDesk": [
                ("Home", self.load_home),
                ("Tenants", self.load_tenants),
                ("Leases", self.load_leases),
                ("Maintenance", self.load_maintenance_staff),
                ("Complaints", self.load_complaints_staff),
                ("Logout", self.logout),
            ],

            "FinanceManager": [
                ("Home", self.load_home),
                ("Payments", self.load_payments),
                ("Reports", self.load_reports),
                ("Logout", self.logout),
            ],

            "MaintenanceStaff": [
                ("Home", self.load_home),
                ("Maintenance", self.load_maintenance_staff),
                ("Complaints", self.load_complaints_staff),
                ("Logout", self.logout),
            ],

            "Manager": [
                ("Home", self.load_home),
                ("Apartments", self.load_apartments),
                ("Reports", self.load_reports),
                ("Logout", self.logout),
            ],
        }

        # TENANT MENU

        tenant_menu = [
            ("Home", self.load_home),
            ("My Lease", self.load_leases),
            ("Payments", self.load_payments),
            ("My Maintenance", self.load_maintenance_tenant),
            ("My Complaints", self.load_complaints_tenant),
            ("Logout", self.logout),
        ]


        # SELECT MENU BASED ON ROLE

        if self.session.is_tenant or self.session.role == "Tenant":
            allowed_menu = tenant_menu
        else:
            allowed_menu = staff_menus.get(self.session.role, [])


        # RENDER BUTTONS

        for text, command in allowed_menu:
            btn = tk.Button(
                self.parent,
                text=text,
                command=command,
                bg="#34495e",
                fg="white",
                relief="flat",
                height=2
            )
            btn.pack(fill="x")

    # PAGE LOADERS

    def load_home(self):
        if self.session.is_tenant:
            from ui.tenant_portal.tenant_dashboard import TenantDashboard
            self.main_window.load_page(TenantDashboard)
        else:
            from ui.home_page import HomePage
            self.main_window.load_page(HomePage)

    # STAFF LOADERS
    def load_tenants(self):
        from ui.tenants.tenants_home import TenantsHome
        self.main_window.load_page(TenantsHome)

    def load_apartments(self):
        from ui.apartments.apartments_home import ApartmentsHome
        self.main_window.load_page(ApartmentsHome)

    def load_leases(self):
        from ui.leases.leases_home import LeasesHome
        self.main_window.load_page(LeasesHome)

    def load_payments(self):
        from ui.payments.payments_home import PaymentsHome
        self.main_window.load_page(PaymentsHome)

    def load_maintenance_staff(self):
        from ui.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(MaintenanceHome)

    def load_complaints_staff(self):
        from ui.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(ComplaintsHome)

    def load_reports(self):
        from ui.reports.reports_home import ReportsHomePage
        self.main_window.load_page(ReportsHomePage)

    def load_users(self):
        from ui.user_management.users_home import UsersHomePage
        self.main_window.load_page(UsersHomePage)

    # TENANT LOADERS
    def load_maintenance_tenant(self):
        from ui.tenant_portal.tenant_maintenance_page import TenantMaintenance
        self.main_window.load_page(TenantMaintenance)

    def load_complaints_tenant(self):
        from ui.tenant_portal.tenant_complaints_page import TenantComplaint
        self.main_window.load_page(TenantComplaint)

    # LOGOUT
    def logout(self):
        self.main_window.destroy()
        from ui.login_page import LoginPage
        LoginPage().mainloop()