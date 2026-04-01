import tkinter as tk
from ui.navigation import Navigation


class MainWindow(tk.Tk):
    """Main application window after login."""

    def __init__(self, user_session):
        super().__init__()

        self.title("Paragon Apartment Management System")
        self.geometry("1200x800")

        # Store the authenticated session (staff or tenant)
        self.user_session = user_session

        # Sidebar navigation
        sidebar = tk.Frame(self, bg="#9a2222", width=200)
        sidebar.pack(side="left", fill="y")

        Navigation(sidebar, self)

        # Main content area
        self.content_frame = tk.Frame(self, bg="white")
        self.content_frame.pack(side="right", fill="both", expand=True)

        # Load initial page based on role
        self.load_home_page()

    def load_home_page(self):
        if self.user_session.role == "Tenant":
            from ui.tenant_portal.tenant_dashboard import TenantDashboard
            self.load_page(lambda parent, mw: TenantDashboard(parent, mw))
        else:
            from ui.home_page import HomePage
            self.load_page(lambda parent, mw: HomePage(parent, mw))

    def load_page(self, page_factory):
        """Replace the content frame with a new page."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        page = page_factory(self.content_frame, self)
        page.pack(fill="both", expand=True)