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

        # Staff
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

        # Tenants
        tenant_menu = [
            ("Home", self.load_home),
            ("My Lease", self.load_lease_tenant),
            ("Payments", self.load_payments_tenant),
            ("Payment Graphs", self.load_payment_graphs_tenant),
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
                bg="#34495e",
                fg="white",
                relief="flat",
                height=2
            ).pack(fill="x")

    # Home
    def load_home(self):
        if self.session.role == "Tenant":
            from ui.tenant_portal.tenant_dashboard import TenantDashboard
            self.main_window.load_page(TenantDashboard)
        else:
            from ui.home_page import HomePage
            self.main_window.load_page(HomePage)

    # Staff loaders
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
        from ui.reports.reports_home import ReportsHome
        self.main_window.load_page(ReportsHome)

    def load_users(self):
        from ui.user_management.users_home import UsersHomePage
        self.main_window.load_page(UsersHomePage)

    # Loaders for tenants
    def load_lease_tenant(self):
        from ui.tenant_portal.lease.lease_view import LeaseView
        self.main_window.load_page(LeaseView)

    def load_payments_tenant(self):
        from ui.tenant_portal.payments.payments_home import PaymentsHome
        self.main_window.load_page(PaymentsHome)

    def load_payment_graphs_tenant(self):
        from ui.tenant_portal.payments.payment_graphs import PaymentGraphs
        self.main_window.load_page(PaymentGraphs)

    def load_maintenance_tenant(self):
        from ui.tenant_portal.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(MaintenanceHome)

    def load_complaints_tenant(self):
        from ui.tenant_portal.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(ComplaintsHome)

    # Logout
    def logout(self):
        self.main_window.destroy()
        from ui.login_page import LoginPage
        LoginPage().mainloop()