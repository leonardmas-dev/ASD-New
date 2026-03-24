import tkinter as tk

class LeasesHome(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Title
        tk.Label(self, text="Lease Management Dashboard", font=("Arial", 20, "bold")).pack(pady=(40, 10))
        tk.Label(self, text="Manage tenant contracts and early termination requests.", font=("Arial", 10)).pack(pady=(0, 30))

        # Button Container
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        # 1. View All Leases (The List)
        list_btn = tk.Button(button_frame, text="View Active Leases", 
                             width=30, height=2, bg="#3498db", fg="white", font=("Arial", 11, "bold"),
                             command=lambda: self.controller.show_frame("LeaseListPage"))
        list_btn.pack(pady=10)

        # 2. Create New Lease
        add_btn = tk.Button(button_frame, text="Create New Lease Agreement", 
                            width=30, height=2, bg="#2ecc71", fg="white", font=("Arial", 11, "bold"),
                            command=lambda: self.controller.show_frame("AddLeasePage"))
        add_btn.pack(pady=10)

        # 3. Handle Termination (Optional direct link)
        # Often managers want to go straight to the list to find the lease to terminate
        
        # 4. Back to Main System Menu
        back_btn = tk.Button(button_frame, text="← Back to Main Menu", 
                             width=30, height=2, bg="#95a5a6", fg="white",
                             command=lambda: self.controller.show_frame("MainMenu"))
        back_btn.pack(pady=30)