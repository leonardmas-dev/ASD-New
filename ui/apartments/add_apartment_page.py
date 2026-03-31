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
    """Create a new apartment."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Add Apartment", font=("Arial", 22)).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        # Apartment Type
        tk.Label(form, text="Apartment Type:").grid(row=0, column=0, sticky="e")
        self.type_combo = ttk.Combobox(form, values=APARTMENT_TYPES, state="readonly")
        self.type_combo.grid(row=0, column=1, padx=5, pady=5)

        # Monthly Rent
        tk.Label(form, text="Monthly Rent (£):").grid(row=1, column=0, sticky="e")
        self.rent_entry = tk.Entry(form)
        self.rent_entry.grid(row=1, column=1, padx=5, pady=5)

        # Number of Rooms
        tk.Label(form, text="Number of Rooms:").grid(row=2, column=0, sticky="e")
        self.rooms_entry = tk.Entry(form)
        self.rooms_entry.grid(row=2, column=1, padx=5, pady=5)

        # Floor Number
        tk.Label(form, text="Floor Number:").grid(row=3, column=0, sticky="e")
        self.floor_entry = tk.Entry(form)
        self.floor_entry.grid(row=3, column=1, padx=5, pady=5)

        # Availability
        tk.Label(form, text="Available:").grid(row=4, column=0, sticky="e")
        self.available_combo = ttk.Combobox(form, values=["Yes", "No"], state="readonly")
        self.available_combo.grid(row=4, column=1, padx=5, pady=5)

        # Active
        tk.Label(form, text="Active:").grid(row=5, column=0, sticky="e")
        self.active_combo = ttk.Combobox(form, values=["Yes", "No"], state="readonly")
        self.active_combo.grid(row=5, column=1, padx=5, pady=5)

        # Location
        tk.Label(form, text="Location:").grid(row=6, column=0, sticky="e")
        self.location_combo = ttk.Combobox(form, state="readonly")
        self.location_combo.grid(row=6, column=1, padx=5, pady=5)

        tk.Button(self, text="Create Apartment", command=self.save).pack(pady=15)

        self._load_locations()

    def _load_locations(self):
        db = get_session()
        locations = db.query(Location).all()
        db.close()

        self.location_map = {
            f"{loc.location_id} - {loc.name}": loc.location_id
            for loc in locations
        }

        self.location_combo["values"] = list(self.location_map.keys())

    def save(self):
        try:
            apt_type = self.type_combo.get()
            rent = int(self.rent_entry.get())
            rooms = int(self.rooms_entry.get())
            floor = int(self.floor_entry.get())
            available = self.available_combo.get() == "Yes"
            active = self.active_combo.get() == "Yes"
            location_id = self.location_map[self.location_combo.get()]
        except Exception:
            messagebox.showerror("Error", "Invalid input.")
            return

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

        messagebox.showinfo("Success", "Apartment created.")