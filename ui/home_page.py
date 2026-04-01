import tkinter as tk
from tkinter import ttk
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

        # Title
        tk.Label(
            container,
            text="Welcome to Paragon Apartments Management System",
            font=("Arial", 26, "bold")
        ).pack(pady=(0, 20))

        # Image path
        image_path = os.path.join("ui", "pamsflats.jpg")

        self.image_label = tk.Label(container)
        self.image_label.pack(pady=10)

        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)

                # Resized
                img = img.resize((600, 300), Image.LANCZOS)
                self.photo = ImageTk.PhotoImage(img)

                self.image_label.config(image=self.photo)

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
                text="(Place 'pamsflats.jpg' in the ui/ folder)",
                bg="#d9d9d9",
                font=("Arial", 12, "italic")
            ).place(relx=0.5, rely=0.5, anchor="center")

        text = (
            "Welcome to the staff portal. From here, you can manage tenants, leases, "
            "payments, maintenance requests, complaints, reports, and user accounts.\n\n"
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