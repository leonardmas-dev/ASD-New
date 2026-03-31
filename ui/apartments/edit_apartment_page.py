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


class EditApartmentPage(tk.Frame):
    """Edit an existing apartment."""

    def __init__(self, parent, main_window, apartment_id):
        super().__init__(parent)

        self.apartment_id = apartment_id

        tk.Label(self, text="Edit Apartment", font=("Arial", 22)).pack(pady=20)

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

        tk.Button(self, text="Save Changes", command=self.save).pack(pady=15)

        self.load_data()

    def load_data(self):
        db = get_session()
        apt = db.query(Apartment).filter(Apartment.apartment_id == self.apartment_id).first()
        db.close()

        self.type_combo.set(apt.apartment_type)
        self.rent_entry.insert(0, apt.monthly_rent)
        self.rooms_entry.insert(0, apt.num_rooms)
        self.floor_entry.insert(0, apt.floor_number)
        self.available_combo.set("Yes" if apt.is_available else "No")
        self.active_combo.set("Yes" if apt.is_active else "No")

    def save(self):
        try:
            apt_type = self.type_combo.get()
            rent = int(self.rent_entry.get())
            rooms = int(self.rooms_entry.get())
            floor = int(self.floor_entry.get())
            available = self.available_combo.get() == "Yes"
            active = self.active_combo.get() == "Yes"
        except Exception:
            messagebox.showerror("Error", "Invalid input.")
            return

        db = get_session()
        apt = db.query(Apartment).filter(Apartment.apartment_id == self.apartment_id).first()

        apt.apartment_type = apt_type
        apt.monthly_rent = rent
        apt.num_rooms = rooms
        apt.floor_number = floor
        apt.is_available = available
        apt.is_active = active

        db.commit()
        db.close()

        messagebox.showinfo("Success", "Apartment updated.")