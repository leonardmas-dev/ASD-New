# Student: Yaseen Sassi     StudentID: 24023127

import tkinter as tk


class Navigation:
    """Role-based navigation system."""

    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.session = main_window.user_session

        self.build_menu()

    def build_menu(self):
        """Build sidebar menu based on user role."""

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
                ("Payments", self.load_payments),
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

        tenant_menu = [
            ("Home", self.load_home),
            ("My Lease", self.load_lease_tenant),
            ("Payments", self.load_payments_tenant),
            ("My Maintenance", self.load_maintenance_tenant),
            ("My Complaints", self.load_complaints_tenant),
            ("Logout", self.logout),
        ]

        if self.session.role == "Tenant":
            allowed_menu = tenant_menu
        else:
            allowed_menu = staff_menus.get(self.session.role, [])

        for text, command in allowed_menu:
            tk.Button(
                self.parent,
                text=text,
                command=command,
                bg="#13325E",
                fg="white",
                relief="flat",
                height=2
            ).pack(fill="x")

    # Home
    def load_home(self):
        if self.session.role == "Tenant":
            from ui.tenant_portal.tenant_dashboard import TenantDashboard
            self.main_window.load_page(lambda parent, mw: TenantDashboard(parent, mw))
        else:
            from ui.home_page import HomePage
            self.main_window.load_page(lambda parent, mw: HomePage(parent, mw))

    # Staff loaders
    def load_tenants(self):
        from ui.tenants.tenants_home import TenantsHome
        self.main_window.load_page(lambda parent, mw: TenantsHome(parent, mw))

    def load_apartments(self):
        from ui.apartments.apartments_home import ApartmentsHome
        self.main_window.load_page(lambda parent, mw: ApartmentsHome(parent, mw))

    def load_leases(self):
        from ui.leases.leases_home import LeasesHome
        self.main_window.load_page(lambda parent, mw: LeasesHome(parent, mw))

    def load_payments(self):
        from ui.payments.payments_home import PaymentsHome
        self.main_window.load_page(lambda parent, mw: PaymentsHome(parent, mw))

    def load_maintenance_staff(self):
        from ui.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(lambda parent, mw: MaintenanceHome(parent, mw))

    def load_complaints_staff(self):
        from ui.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(lambda parent, mw: ComplaintsHome(parent, mw))

    def load_reports(self):
        from ui.reports.reports_home import ReportsHome
        self.main_window.load_page(lambda parent, mw: ReportsHome(parent, mw))

    def load_users(self):
        from ui.user_management.users_home import UsersHomePage
        self.main_window.load_page(lambda parent, mw: UsersHomePage(parent, mw))

    # Tenant loaders
    def load_lease_tenant(self):
        from ui.tenant_portal.lease.lease_view import LeaseView
        self.main_window.load_page(lambda parent, mw: LeaseView(parent, mw))

    def load_payments_tenant(self):
        from ui.tenant_portal.payments.payments_home import PaymentsHome
        self.main_window.load_page(lambda parent, mw: PaymentsHome(parent, mw))

    def load_maintenance_tenant(self):
        from ui.tenant_portal.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(lambda parent, mw: MaintenanceHome(parent, mw))

    def load_complaints_tenant(self):
        from ui.tenant_portal.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(lambda parent, mw: ComplaintsHome(parent, mw))

    # Logout
    def logout(self):
        self.main_window.destroy()
        from ui.login_page import LoginPage
        LoginPage().mainloop()