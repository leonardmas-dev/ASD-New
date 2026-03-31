import tkinter as tk
from tkinter import ttk

from database.session import get_session
from database.models import Lease


class LeaseView(tk.Frame):
    """Tenant view of their active lease."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session

        db = get_session()

        # get active lease
        lease = (
            db.query(Lease)
            .filter(
                Lease.tenant_id == self.session.tenant_id,
                Lease.is_active == True,
            )
            .first()
        )

        if not lease:
            tk.Label(self, text="No active lease found.", font=("Arial", 16)).pack(pady=20)
            db.close()
            return

        # extract all needed values BEFORE closing session
        apt = lease.apartment
        loc = apt.location

        lease_data = {
            "Apartment ID": apt.apartment_id,
            "City": loc.city,
            "Postcode": loc.postcode,
            "Monthly Rent": f"£{lease.monthly_rent}",
            "Start Date": lease.start_date.strftime("%Y-%m-%d"),
            "End Date": lease.end_date.strftime("%Y-%m-%d"),
            "Deposit": f"£{lease.deposit_amount}",
        }

        db.close()

        tk.Label(self, text="My Lease Details", font=("Arial", 22)).pack(pady=20)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        for label, value in lease_data.items():
            row = tk.Frame(frame)
            row.pack(anchor="w", pady=3)
            tk.Label(row, text=f"{label}: ", font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(row, text=value, font=("Arial", 12)).pack(side="left")

        # back to dashboard
        tk.Button(
            self,
            text="Back to Dashboard",
            command=self.go_home
        ).pack(pady=20)

    # back to dashboard
    def go_home(self):
        from ui.tenant_portal.tenant_dashboard import TenantDashboard
        self.main_window.load_page(TenantDashboard)