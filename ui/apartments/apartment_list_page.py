import tkinter as tk
from tkinter import ttk

from database.session import get_session
from database.models import Apartment, Location


class ApartmentListPage(tk.Frame):
    """List of apartments for selection."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Select Apartment", font=("Arial", 22)).pack(pady=20)

        self.table = ttk.Treeview(
            self,
            columns=("id", "location", "type", "rooms", "active"),
            show="headings",
        )

        headings = [
            ("id", "ID"),
            ("location", "Location"),
            ("type", "Type"),
            ("rooms", "Rooms"),
            ("active", "Active"),
        ]

        for col, text in headings:
            self.table.heading(col, text=text)

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

    def load_data(self):
        db = get_session()
        apartments = db.query(Apartment).join(Location).all()
        db.close()

        for apt in apartments:
            self.table.insert(
                "",
                "end",
                values=(
                    apt.apartment_id,
                    apt.location.name, 
                    apt.apartment_type,
                    apt.num_rooms,
                    "Yes" if apt.is_active else "No",
                ),
            )