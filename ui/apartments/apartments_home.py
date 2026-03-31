import tkinter as tk
from tkinter import ttk
from database.session import get_session
from database.models import Apartment, Location

class ApartmentsHome(tk.Frame):
    """Staff overview of all apartments."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Apartments", font=("Arial", 22)).pack(pady=20)
        # buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Apartment",
            width=18,
            command=self.open_add_page
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Edit Apartment",
            width=18,
            command=self.open_edit_page
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="View Apartment List",
            width=18,
            command=self.open_list_page
        ).grid(row=0, column=2, padx=5)

        # table
        self.table = ttk.Treeview(
            self,
            columns=("id", "location", "type", "rooms", "rent", "floor", "available", "active"),
            show="headings",
        )

        headings = [
            ("id", "ID"),
            ("location", "Location"),
            ("type", "Type"),
            ("rooms", "Rooms"),
            ("rent", "Rent (£)"),
            ("floor", "Floor"),
            ("available", "Available"),
            ("active", "Active"),
        ]

        for col, text in headings:
            self.table.heading(col, text=text)

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

    # load apartments into table
    def load_data(self):
        db = get_session()
        apartments = db.query(Apartment).join(Location).all()

        # load all rows before closing session
        rows = []
        for apt in apartments:
            rows.append((
                apt.apartment_id,
                apt.location.name,
                apt.apartment_type,
                apt.num_rooms,
                apt.monthly_rent,
                apt.floor_number,
                "Yes" if apt.is_available else "No",
                "Yes" if apt.is_active else "No",
            ))

        db.close()

        for row in rows:
            self.table.insert("", "end", values=row)

    # add apartments page
    def open_add_page(self):
        from ui.apartments.add_apartment_page import AddApartmentPage
        self.main_window.load_page(AddApartmentPage)
    # edit apartments page
    def open_edit_page(self):
        from ui.apartments.edit_apartment_page import EditApartmentPage
        self.main_window.load_page(EditApartmentPage)
    # apartment list page
    def open_list_page(self):
        from ui.apartments.apartment_list_page import ApartmentListPage
        self.main_window.load_page(ApartmentListPage)