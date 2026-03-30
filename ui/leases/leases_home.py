import tkinter as tk
# Import the actual classes for the teammate's load_page system
from ui.leases.lease_list_page import LeaseListPage
from ui.leases.add_lease_page import AddLeasePage

class LeasesHome(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller # This is the main_window/app.py

        # Title
        tk.Label(self, text="Lease Management Dashboard", font=("Arial", 20, "bold")).pack(pady=(40, 10))
        tk.Label(self, text="Manage tenant contracts and early termination requests.", font=("Arial", 10)).pack(pady=(0, 30))

        # Button Container
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # 1. View All Leases (Points to LeaseListPage class)
        list_btn = tk.Button(button_frame, text="View Active Leases", 
                             width=30, height=2, bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                             command=lambda: self.controller.load_page(LeaseListPage))
        list_btn.pack(pady=10)

        # 2. Create New Lease (Points to AddLeasePage class)
        add_btn = tk.Button(button_frame, text="Create New Lease Agreement", 
                            width=30, height=2, bg="#2ecc71", fg="white", font=("Arial", 11, "bold"),
                            command=lambda: self.controller.load_page(AddLeasePage))
        add_btn.pack(pady=10)
