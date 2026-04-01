import tkinter as tk
from PIL import Image, ImageTk
import os

class TenantDashboard(tk.Frame):
    """Tenant dashboard."""
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.session = main_window.user_session
        tk.Label(self, text="Welcome to Your Tenant Portal", font=("Arial", 26, "bold")).pack(pady=20)
        # text for intro
        intro = (
            "This portal gives you quick access to everything related to your tenancy.\n\n"
            "Use the navigation menu on the left to:\n"
            " • View your lease details\n"
            " • Make and track payments\n"
            " • Submit and monitor maintenance requests\n"
            " • File and follow up on complaints\n\n"
            "Everything you need is just one click away."
        )
        tk.Label(self, text=intro, font=("Arial", 14), justify="left").pack(pady=10)
        # Image for a stock photo
        image_path = os.path.join("ui", "apartment_interior.jpg")
        self.image_label = tk.Label(self)
        self.image_label.pack(pady=20)
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((600, 350), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=photo)
                self.image_label.image = photo
            except Exception:
                self.image_label.config(
                    text="(Image could not be loaded)",
                    font=("Arial", 12, "italic")
                )
        else:
            placeholder = tk.Frame(self.image_label, width=600, height=350, bg="#d9d9d9")
            placeholder.pack()
            tk.Label(
                placeholder,
                text="image",
                bg="#d9d9d9",
                font=("Arial", 12, "italic")
            ).place(relx=0.5, rely=0.5, anchor="center")