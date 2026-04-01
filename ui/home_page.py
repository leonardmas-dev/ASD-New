import tkinter as tk
from PIL import Image, ImageTk
import os
class HomePage(tk.Frame):
    """Staff home page with welcome text and apartment image."""
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session
        container = tk.Frame(self)
        container.pack(pady=40)
        tk.Label(
            container,
            text="Welcome to Paragon Apartments Management System",
            font=("Arial", 26, "bold")
        ).pack(pady=(0, 20))
        image_path = os.path.join("ui", "apartments.jpeg")
        self.image_label = tk.Label(container)
        self.image_label.pack(pady=10)
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((600, 300), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo)
                self.image_label.image = photo
            except Exception:
                self.image_label.config(
                    text="(Image could not be loaded)",
                    font=("Arial", 12, "italic")
                )
        else:
            placeholder = tk.Frame(self.image_label, width=600, height=300, bg="#d9d9d9")
            placeholder.pack()
            tk.Label(
                placeholder,
                text="image",
                bg="#d9d9d9",
                font=("Arial", 12, "italic")
            ).place(relx=0.5, rely=0.5, anchor="center")
        text = (
            "Welcome to the staff portal. From here, staff members can manage various modules such as tenants, apartments, leases, "
            "payments, maintenance requests, complaints, reports, and user accounts depending on access levels.\n\n"
            "Use the navigation bar on the left to access the different modules and "
            "perform your daily tasks efficiently."
        )
        tk.Label(
            container,
            text=text,
            font=("Arial", 14),
            justify="center",
            wraplength=750
        ).pack(pady=20)