import tkinter as tk
from tkinter import ttk, messagebox

class AddApartmentPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
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

        # Submit Button
        submit_btn = tk.Button(self, text="Save Apartment", command=self.save_data, bg="green", fg="white")
        submit_btn.grid(row=5, column=0, columnspan=2, pady=20)

    def save_data(self):
        # Validation Logic
        location = self.location_cb.get()
        rent = self.rent_entry.get()
        
        if not location or not rent:
            messagebox.showerror("Error", "All fields are required!")
            return
        
        try:
            float(rent) # Ensure rent is a number
        except ValueError:
            messagebox.showerror("Error", "Rent must be a valid number.")
            return

        # Here you will call your backend/apartment_service.py
        print(f"Saving Apartment in {location} for £{rent}")
        messagebox.showinfo("Success", "Apartment registered successfully!")