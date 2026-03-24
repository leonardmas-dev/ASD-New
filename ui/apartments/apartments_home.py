import tkinter as tk

class ApartmentsHome(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title Section
        tk.Label(self, text="Apartment Management Dashboard", font=("Arial", 20, "bold")).pack(pady=(40, 10))
        tk.Label(self, text="Select an action below to manage property inventory.", font=("Arial", 10)).pack(pady=(0, 30))

        # Button Container (to keep them centered and neat)
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # 1. Button to View List
        view_btn = tk.Button(button_frame, text="View Apartment Inventory", 
                             width=30, height=2, bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                             command=lambda: self.controller.show_frame("ApartmentListPage"))
        view_btn.pack(pady=10)

        # 2. Button to Add New
        add_btn = tk.Button(button_frame, text="Register New Apartment", 
                            width=30, height=2, bg="#2ecc71", fg="white", font=("Arial", 11, "bold"),
                            command=lambda: self.controller.show_frame("AddApartmentPage"))
        add_btn.pack(pady=10)

        # 3. Back to Main System Menu
        back_btn = tk.Button(button_frame, text="← Back to Main Menu", 
                             width=30, height=2, bg="#95a5a6", fg="white",
                             command=lambda: self.controller.show_frame("MainMenu"))
        back_btn.pack(pady=30)