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
        # Menu config per role
        role_menus = {
            "Admin": [
                ("Home", self.load_home),
                ("Tenants", self.load_tenants),
                ("Apartments", self.load_apartments),
                ("Leases", self.load_leases),
                ("Payments", self.load_payments),
                ("Maintenance", self.load_maintenance),
                ("Complaints", self.load_complaints),
                ("Reports", self.load_reports),
                ("User Management", self.load_users),
                ("Logout", self.logout),
            ],

            "FrontDesk": [
                ("Home", self.load_home),
                ("Tenants", self.load_tenants),
                ("Leases", self.load_leases),
                ("Maintenance", self.load_maintenance),
                ("Complaints", self.load_complaints),
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
                ("Maintenance", self.load_maintenance),
                ("Complaints", self.load_complaints),
                ("Logout", self.logout),
            ],

            "Manager": [
                ("Home", self.load_home),
                ("Apartments", self.load_apartments),
                ("Reports", self.load_reports),
                ("Logout", self.logout),
            ],

            "Tenant": [
                ("Home", self.load_home),
                ("My Lease", self.load_leases),
                ("Payments", self.load_payments),
                ("Maintenance", self.load_maintenance),
                ("Complaints", self.load_complaints),
                ("Logout", self.logout),
            ],
        }

        # Get allowed menu for this user
        allowed_menu = role_menus.get(self.session.role, [])

        # Create buttons for allowed items
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

    # Page loaders
    def load_home(self):
        from ui.home_page import HomePage
        self.main_window.load_page(HomePage)

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

    def load_maintenance(self):
        from ui.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(MaintenanceHome)

    def load_complaints(self):
        from ui.complaints.complaints_home import ComplaintsHome
        self.main_window.load_page(ComplaintsHome)

    def load_reports(self):
        from ui.reports.reports_home import ReportsHome
        self.main_window.load_page(ReportsHome)

    def load_users(self):
        from ui.user_management.users_home import UsersHome
        self.main_window.load_page(UsersHome)
    
    def logout(self):
        self.main_window.destroy()
        # Return to login page
        from ui.login_page import LoginPage
        LoginPage().mainloop()