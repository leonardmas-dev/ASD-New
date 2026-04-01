import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database.session import get_session
from database.models import Apartment, Location, Lease
from sqlalchemy.orm import joinedload


class ApartmentsHome(tk.Frame):
    """Staff overview of all apartments, including occupancy."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Apartments", font=("Arial", 22)).pack(pady=20)

        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="Filter by Location:").pack(side="left", padx=5)

        self.location_filter = ttk.Combobox(filter_frame, state="readonly", width=20)
        self.location_filter.pack(side="left", padx=5)

        self.location_filter.bind("<<ComboboxSelected>>", lambda e: self.refresh())

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Apartment",
            width=18,
            command=self.open_add_page,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Edit Apartment",
            width=18,
            command=self.open_edit_page,
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="Assign to Tenant",
            width=18,
            command=self.open_assign_page,
        ).grid(row=0, column=2, padx=5)

        tk.Button(
            btn_frame,
            text="End Lease / Vacate",
            width=18,
            command=self.end_lease,
        ).grid(row=0, column=3, padx=5)

        tk.Button(
            btn_frame,
            text="Refresh",
            width=18,
            command=self.refresh,
        ).grid(row=0, column=4, padx=5)
        table_container = tk.Frame(self)
        table_container.pack(fill="both", expand=True, pady=10)

        x_scroll = tk.Scrollbar(table_container, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")

        y_scroll = tk.Scrollbar(table_container, orient="vertical")
        y_scroll.pack(side="right", fill="y")

        self.table = ttk.Treeview(
            table_container,
            columns=("id", "location", "type", "rooms", "rent", "floor", "available", "active", "tenant"),
            show="headings",
            xscrollcommand=x_scroll.set,
            yscrollcommand=y_scroll.set,
        )
        self.table.pack(fill="both", expand=True)
        x_scroll.config(command=self.table.xview)
        y_scroll.config(command=self.table.yview)
        headings = [
            ("id", "ID"),
            ("location", "Location"),
            ("type", "Type"),
            ("rooms", "Rooms"),
            ("rent", "Rent (£)"),
            ("floor", "Floor"),
            ("available", "Available"),
            ("active", "Active"),
            ("tenant", "Current Tenant"),
        ]

        for col, text in headings:
            self.table.heading(col, text=text)

        # Keep ID column hidden like before
        self.table.column("id", width=0, stretch=False)

        self.load_locations()
        self.load_data()

    # Load dropdown locations
    def load_locations(self):
        db = get_session()
        locations = db.query(Location).all()
        db.close()

        names = ["All"] + [loc.name for loc in locations]
        self.location_filter["values"] = names
        self.location_filter.set("All")

    def refresh(self):
        for row in self.table.get_children():
            self.table.delete(row)
        self.load_data()

    # Load apartment data
    def load_data(self):
        db = get_session()

        selected_location = self.location_filter.get()

        query = (
            db.query(Apartment)
            .options(joinedload(Apartment.location), joinedload(Apartment.leases))
        )

        if selected_location and selected_location != "All":
            query = query.join(Apartment.location).filter(Location.name == selected_location)

        apartments = query.all()
        now = datetime.utcnow()

        for apt in apartments:
            active_lease = None
            for lease in apt.leases:
                if lease.is_active and lease.start_date <= now <= lease.end_date:
                    active_lease = lease
                    break

            tenant_name = ""
            if active_lease and active_lease.tenant:
                t = active_lease.tenant
                tenant_name = f"{t.first_name} {t.last_name}"

            self.table.insert(
                "",
                "end",
                values=(
                    apt.apartment_id,
                    apt.location.name,
                    apt.apartment_type,
                    apt.num_rooms,
                    apt.monthly_rent,
                    apt.floor_number,
                    "Yes" if apt.is_available else "No",
                    "Yes" if apt.is_active else "No",
                    tenant_name,
                ),
            )

        db.close()

    def _get_selected_apartment_id(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showerror("Error", "Please select an apartment first.")
            return None
        values = self.table.item(selected[0], "values")
        return int(values[0])

    def open_add_page(self):
        from ui.apartments.add_apartment_page import AddApartmentPage
        self.main_window.load_page(AddApartmentPage)

    def open_edit_page(self):
        from ui.apartments.edit_apartment_page import EditApartmentPage
        apt_id = self._get_selected_apartment_id()
        if apt_id is None:
            return
        self.main_window.load_page(
            lambda parent, mw: EditApartmentPage(parent, mw, apt_id)
        )

    def open_assign_page(self):
        from ui.apartments.assign_apartment_page import AssignApartmentPage
        apt_id = self._get_selected_apartment_id()
        if apt_id is None:
            return
        self.main_window.load_page(
            lambda parent, mw: AssignApartmentPage(parent, mw, apt_id)
        )

    def end_lease(self):
        from database.models import Lease

        apt_id = self._get_selected_apartment_id()
        if apt_id is None:
            return

        db = get_session()
        now = datetime.utcnow()

        apt = db.query(Apartment).filter(Apartment.apartment_id == apt_id).first()
        if not apt:
            db.close()
            messagebox.showerror("Error", "Apartment not found.")
            return

        active_lease = (
            db.query(Lease)
            .filter(
                Lease.apartment_id == apt_id,
                Lease.is_active == True,
                Lease.start_date <= now,
                Lease.end_date >= now,
            )
            .first()
        )

        if not active_lease:
            db.close()
            messagebox.showinfo("Info", "No active lease found for this apartment.")
            return

        active_lease.is_active = False
        apt.is_available = True

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Lease ended and apartment vacated.")
        self.refresh()