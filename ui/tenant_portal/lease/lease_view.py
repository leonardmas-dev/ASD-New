import tkinter as tk

from backend.payment_service import PaymentService


class LeaseViewPage(tk.Frame):
    """
    Displays the tenant's active lease details.
    Mirrors real-world tenant portals where users can view their lease info.
    """

    def __init__(self, parent, main_window):
        super().__init__(parent)

        # Store references
        self.main_window = main_window
        self.session = main_window.user_session
        self.tenant_id = self.session.tenant_id

        self.service = PaymentService()

        # Header
        tk.Label(self, text="My Lease", font=("Arial", 18, "bold")).pack(pady=20)

        # Fetch active lease
        self.lease = self.service.get_current_active_lease_for_tenant(self.tenant_id)

        # If no active lease, show message + back button
        if not self.lease:
            tk.Label(self, text="No active lease found.").pack(pady=10)
            self.add_back_button()
            return

        # Lease Details Container
        container = tk.Frame(self)
        container.pack(pady=10)

        # Extract apartment + location info
        apt = self.lease.apartment
        loc = apt.location

        details = [
            ("Lease ID:", self.lease.lease_id),
            ("Apartment ID:", apt.apartment_id),
            ("City:", loc.city),
            ("Address:", loc.address),
            ("Monthly Rent (£):", apt.rent_amount),
            ("Start Date:", self.lease.start_date),
            ("End Date:", self.lease.end_date),
            ("Status:", "Active" if self.lease.is_active else "Inactive"),
        ]

        for i, (label, value) in enumerate(details):
            tk.Label(container, text=label, anchor="w", width=20).grid(row=i, column=0, sticky="w", pady=3)
            tk.Label(container, text=str(value), anchor="w").grid(row=i, column=1, sticky="w", pady=3)

        self.add_back_button()

    # Back Button
    def add_back_button(self):
        from ui.tenant_portal.dashboard.tenant_dashboard import TenantDashboard
        tk.Button(
            self,
            text="Back",
            command=lambda: self.main_window.load_page(TenantDashboard),
        ).pack(pady=20)