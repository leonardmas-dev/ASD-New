import tkinter as tk
from datetime import datetime

from database.session import get_session
from database.models import Lease


class LeaseView(tk.Frame):
    """Tenant view of their active lease and apartment details."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.session = main_window.user_session

        tk.Label(self, text="My Lease Details", font=("Arial", 22)).pack(pady=20)

        self.container = tk.Frame(self)
        self.container.pack(pady=10)

        self.load_data()

        tk.Button(
            self,
            text="Back to Dashboard",
            command=self.go_home
        ).pack(pady=20)

    def load_data(self):
        db = get_session()
        now = datetime.utcnow()

        lease = (
            db.query(Lease)
            .filter(
                Lease.tenant_id == self.session.tenant_id,
                Lease.is_active == True,
                Lease.start_date <= now,
                Lease.end_date >= now,
            )
            .first()
        )

        if not lease:
            db.close()
            tk.Label(
                self.container,
                text="No active lease found.",
                font=("Arial", 16)
            ).pack(pady=20)
            return

        apt = lease.apartment
        loc = apt.location

        lease_data = {
            "Apartment Type": apt.apartment_type,
            "Rooms": apt.num_rooms,
            "Floor": apt.floor_number,
            "Monthly Rent": f"£{lease.monthly_rent}",
            "Deposit": f"£{lease.deposit_amount}",
            "Location": loc.name,
            "City": loc.city,
            "Postcode": loc.postcode,
            "Start Date": lease.start_date.strftime("%Y-%m-%d"),
            "End Date": lease.end_date.strftime("%Y-%m-%d"),
            "Status": "Active",
        }

        db.close()

        for label, value in lease_data.items():
            row = tk.Frame(self.container)
            row.pack(anchor="w", pady=3)

            tk.Label(
                row,
                text=f"{label}: ",
                font=("Arial", 12, "bold")
            ).pack(side="left")

            tk.Label(
                row,
                text=value,
                font=("Arial", 12)
            ).pack(side="left")

    def go_home(self):
        from ui.tenant_portal.tenant_dashboard import TenantDashboard
        self.main_window.load_page(lambda parent, mw: TenantDashboard(parent, mw))