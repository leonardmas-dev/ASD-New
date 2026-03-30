import tkinter as tk
from ui.apartments.apartment_list_page import ApartmentListPage
from ui.apartments.add_apartment_page import AddApartmentPage

class ApartmentsHome(tk.Frame):
    def __init__(self, parent, main_window): # main_window
        super().__init__(parent)
        self.main_window = main_window 

        # Title Section
        tk.Label(self, text="Apartment Management Dashboard", font=("Arial", 20, "bold")).pack(pady=(40, 10))
        tk.Label(self, text="Select an action below to manage property inventory.", font=("Arial", 10)).pack(pady=(0, 30))

        # Button Container
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # 1. View List 
        tk.Button(button_frame, text="View Apartment Inventory", 
        width=30, height=2, bg="#3498db", fg="white", font=("Arial", 11, "bold"),
        command=lambda: self.main_window.load_page(ApartmentListPage)).pack(pady=10)

        # 2. Add New
        tk.Button(button_frame, text="Register New Apartment", 
        width=30, height=2, bg="#2ecc71", fg="white", font=("Arial", 11, "bold"),
        command=lambda: self.main_window.load_page(AddApartmentPage)).pack(pady=10)
