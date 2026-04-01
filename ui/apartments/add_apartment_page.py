# Student: Thierno Batiga     StudentID: 24024769

import tkinter as tk
from tkinter import ttk, messagebox

from database.session import get_session
from database.models import Apartment, Location

APARTMENT_TYPES = [
    "Studio",
    "1-Bed",
    "2-Bed",
    "3-Bed",
    "4-Bed",
    "Penthouse",
    "Accessible Unit",
    "Luxury Unit",
]


class AddApartmentPage(tk.Frame):
    """Create a new apartment with validation."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Add Apartment", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Apartment Type:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.type_combo = ttk.Combobox(form, values=APARTMENT_TYPES, state="readonly", width=30)
        self.type_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form, text="Monthly Rent (£):").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.rent_entry = tk.Entry(form, width=32)
        self.rent_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form, text="Number of Rooms:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.rooms_entry = tk.Entry(form, width=32)
        self.rooms_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form, text="Floor Number:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.floor_entry = tk.Entry(form, width=32)
        self.floor_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(form, text="Available:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.available_combo = ttk.Combobox(form, values=["Yes", "No"], state="readonly", width=30)
        self.available_combo.grid(row=4, column=1, padx=5, pady=5)

        tk.Label(form, text="Active:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.active_combo = ttk.Combobox(form, values=["Yes", "No"], state="readonly", width=30)
        self.active_combo.grid(row=5, column=1, padx=5, pady=5)

        tk.Label(form, text="Location:").grid(row=6, column=0, sticky="e", padx=5, pady=5)
        self.location_combo = ttk.Combobox(form, state="readonly", width=30)
        self.location_combo.grid(row=6, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Create Apartment", width=18, command=self.save).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", width=18, command=self.go_back).grid(row=0, column=1, padx=5)

        self._load_locations()

    def _load_locations(self):
        db = get_session()
        locations = db.query(Location).filter(Location.is_active == True).all()
        db.close()

        self.location_map = {
            f"{loc.location_id} - {loc.name}": loc.location_id
            for loc in locations
        }

        self.location_combo["values"] = list(self.location_map.keys())
        if self.location_map:
            self.location_combo.current(0)

    def save(self):
        apt_type = self.type_combo.get().strip()
        rent_raw = self.rent_entry.get().strip()
        rooms_raw = self.rooms_entry.get().strip()
        floor_raw = self.floor_entry.get().strip()
        available_label = self.available_combo.get().strip()
        active_label = self.active_combo.get().strip()
        location_label = self.location_combo.get().strip()

        if not all([apt_type, rent_raw, rooms_raw, floor_raw, available_label, active_label, location_label]):
            messagebox.showerror("Error", "All fields are required.")
            return

        if apt_type not in APARTMENT_TYPES:
            messagebox.showerror("Error", "Invalid apartment type.")
            return

        try:
            rent = int(rent_raw)
            rooms = int(rooms_raw)
            floor = int(floor_raw)
        except ValueError:
            messagebox.showerror("Error", "Rent, rooms, and floor must be whole numbers.")
            return

        if rent <= 0:
            messagebox.showerror("Error", "Monthly rent must be greater than 0.")
            return

        if rooms <= 0:
            messagebox.showerror("Error", "Number of rooms must be greater than 0.")
            return

        if floor < -2 or floor > 100:
            messagebox.showerror("Error", "Floor number must be between -2 and 100.")
            return

        available = available_label == "Yes"
        active = active_label == "Yes"

        if location_label not in self.location_map:
            messagebox.showerror("Error", "Invalid location selected.")
            return

        location_id = self.location_map[location_label]

        db = get_session()

        apt = Apartment(
            apartment_type=apt_type,
            monthly_rent=rent,
            num_rooms=rooms,
            floor_number=floor,
            is_available=available,
            is_active=active,
            location_id=location_id,
        )

        db.add(apt)
        db.commit()
        db.close()

        messagebox.showinfo("Success", "Apartment created successfully.")
        self.go_back()

    def go_back(self):
        from ui.apartments.apartments_home import ApartmentsHome
        self.main_window.load_page(ApartmentsHome)