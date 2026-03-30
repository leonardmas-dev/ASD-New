import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Fix for "ModuleNotFoundError"
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Import backend and the Home page for navigation
from backend.apartment_service import add_apartment

class AddApartmentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # This is the main_window
        
        # Title
        label = tk.Label(self, text="Register New Apartment", font=("Arial", 18, "bold"))
        label.grid(row=0, column=0, columnspan=2, pady=20)

        # 1. Location Dropdown 
        tk.Label(self, text="Location:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.location_cb = ttk.Combobox(self, values=["Bristol", "Cardiff", "London", "Manchester"])
        self.location_cb.grid(row=1, column=1, padx=10, pady=5)

        # 2. Apartment Type
        tk.Label(self, text="Type:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.type_cb = ttk.Combobox(self, values=["Studio", "1-Bedroom", "2-Bedroom", "Penthouse"])
        self.type_cb.grid(row=2, column=1, padx=10, pady=5)

        # 3. Monthly Rent
        tk.Label(self, text="Monthly Rent (£):").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.rent_entry = tk.Entry(self)
        self.rent_entry.grid(row=3, column=1, padx=10, pady=5)

        # 4. Number of Rooms
        tk.Label(self, text="Number of Rooms:").grid(row=4, column=0, sticky="e", padx=10, pady=5)
        self.rooms_entry = tk.Entry(self)
        self.rooms_entry.grid(row=4, column=1, padx=10, pady=5)

        # 5. Floor Number 
        tk.Label(self, text="Floor Number:").grid(row=5, column=0, sticky="e", padx=10, pady=5)
        self.floor_entry = tk.Entry(self)
        self.floor_entry.grid(row=5, column=1, padx=10, pady=5)

        # Button Container for horizontal layout
        btn_frame = tk.Frame(self)
        btn_frame.grid(row=6, column=0, columnspan=2, pady=20)

        # Submit Button
        submit_btn = tk.Button(btn_frame, text="Save Apartment", command=self.save_data, 
                               bg="green", fg="white", width=15)
        submit_btn.pack(side="left", padx=10)

        # Back Button
        from ui.apartments.apartments_home import ApartmentsHome
        back_btn = tk.Button(btn_frame, text="Back", 
                             command=lambda: self.controller.load_page(ApartmentsHome), 
                             bg="#95a5a6", fg="white", width=15)
        back_btn.pack(side="left", padx=10)

    def save_data(self):
        location = self.location_cb.get()
        apt_type = self.type_cb.get()
        rent = self.rent_entry.get()
        rooms = self.rooms_entry.get()
        floor = self.floor_entry.get() or "1"
        
        if not location or not rent or not rooms:
            messagebox.showerror("Error", "Location, Rent, and Rooms are required!")
            return
        
        try:
            float(rent) 
            int(rooms)
            int(floor)
        except ValueError:
            messagebox.showerror("Error", "Rent, Rooms, and Floor must be valid numbers.")
            return

        success = add_apartment(location, apt_type, rent, rooms, floor)
        
        if success:
            messagebox.showinfo("Success", f"Apartment in {location} registered successfully!")
            self.clear_fields()
            # Optional: Redirect to inventory list after saving
            from ui.apartments.apartment_list_page import ApartmentListPage
            self.controller.load_page(ApartmentListPage)
        else:
            messagebox.showerror("Database Error", "Failed to save to MySQL. Check your connection.")

    def clear_fields(self):
        self.location_cb.set('')
        self.type_cb.set('')
        self.rent_entry.delete(0, tk.END)
        self.rooms_entry.delete(0, tk.END)
        self.floor_entry.delete(0, tk.END)