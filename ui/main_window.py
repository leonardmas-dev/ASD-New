import tkinter as tk
from ui.navigation import Navigation
from database.session import get_session
from database.models import User, Tenant


class MainWindow(tk.Tk):
    """Main application window with full role-based access."""
    def __init__(self, user_id):
        super().__init__()

        self.title("Paragon Apartment Management System")
        self.geometry("1200x750")

        self.user_id = user_id
        self.user_session = self._load_user_session()

        # Sidebar
        self.nav = Navigation(self.sidebar_frame(), self)

        # Main content area
        self.content_frame = tk.Frame(self)
        self.content_frame.pack(side="right", fill="both", expand=True)

        self.current_page = None
        self._load_initial_page()

    def _load_user_session(self):
        """Load user role and tenant_id (if applicable)."""
        db = get_session()
        user = db.query(User).filter(User.user_id == self.user_id).first()

        session = type("Session", (), {})()
        session.user_id = user.user_id
        session.role = user.role  # Admin, FrontDesk, FinanceManager, MaintenanceStaff, Manager, Tenant

        # If tenant, load tenant_id
        if user.role == "Tenant":
            tenant = db.query(Tenant).filter(Tenant.user_id == user.user_id).first()
            session.tenant_id = tenant.tenant_id

        db.close()
        return session

    def sidebar_frame(self):
        """Create and return the sidebar frame."""
        sidebar = tk.Frame(self, width=220, bg="#2c3e50")
        sidebar.pack(side="left", fill="y")
        return sidebar

    def _load_initial_page(self):
        """Load the correct home page based on role."""
        if self.user_session.role == "Tenant":
            from ui.tenant_portal.tenant_dashboard import TenantDashboard
            self.load_page(TenantDashboard)
        else:
            from ui.home_page import HomePage
            self.load_page(HomePage)

    def load_page(self, page_class):
        """Destroy current page and load a new one."""
        if self.current_page:
            self.current_page.destroy()

        self.current_page = page_class(self.content_frame, self)
        self.current_page.pack(fill="both", expand=True)