import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database.session import SessionLocal
from backend.apartment_service import ApartmentService


class EditApartmentPage(tk.Frame):
    def __init__(
        self,
        parent,
        controller,
        apt_id=None,
        location="",
        apt_type="",
        rent="",
        status="",
        **kwargs,
    ):
        super().__init__(parent)
        self.controller = controller
        self.current_apt_id = apt_id

        tk.Label(self, text="Edit Apartment Details", font=("Arial", 18, "bold")).pack(pady=20)

        form_frame = tk.Frame(self)
        form_frame.pack(pady=10)

        tk.Label(form_frame, text="Location:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.location_cb = ttk.Combobox(form_frame, values=["Bristol", "Cardiff", "London", "Manchester"])
        self.location_cb.grid(row=0, column=1, padx=10, pady=5)
        self.location_cb.set(location)

        tk.Label(form_frame, text="Type:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.type_cb = ttk.Combobox(form_frame, values=["Studio", "1-Bedroom", "2-Bedroom", "Penthouse"])
        self.type_cb.grid(row=1, column=1, padx=10, pady=5)
        self.type_cb.set(apt_type)

        tk.Label(form_frame, text="Monthly Rent (£):").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.rent_entry = tk.Entry(form_frame)
        self.rent_entry.grid(row=2, column=1, padx=10, pady=5)
        self.rent_entry.insert(0, str(rent).replace('£', ''))

        tk.Label(form_frame, text="Status:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.status_cb = ttk.Combobox(form_frame, values=["Available", "Occupied", "Maintenance"])
        self.status_cb.grid(row=3, column=1, padx=10, pady=5)
        self.status_cb.set(status)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=30)

        from ui.apartments.apartment_list_page import ApartmentListPage

        tk.Button(
            btn_frame,
            text="Update Apartment",
            bg="#f39c12",
            fg="white",
            width=15,
            command=self.update_data,
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Delete Record",
            bg="#e74c3c",
            fg="white",
            width=15,
            command=self.confirm_delete,
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Cancel",
            command=lambda: self.controller.load_page(ApartmentListPage),
        ).pack(side="left", padx=10)

    def update_data(self):
        if not self.current_apt_id:
            return

        db = SessionLocal()
        service = ApartmentService(db)
        try:
            success = service.update_apartment(
                self.current_apt_id,
                self.location_cb.get(),
                self.type_cb.get(),
                self.rent_entry.get(),
                self.status_cb.get(),
            )
        finally:
            db.close()

        if success:
            messagebox.showinfo("Success", "Apartment details updated.")
            from ui.apartments.apartment_list_page import ApartmentListPage
            self.controller.load_page(ApartmentListPage)
        else:
            messagebox.showerror("Error", "Failed to update database.")

    def confirm_delete(self):
        if not self.current_apt_id:
            return

        answer = messagebox.askyesno("Confirm Delete", "Are you sure you want to remove this apartment?")
        if not answer:
            return

        db = SessionLocal()
        service = ApartmentService(db)
        try:
            success = service.delete_apartment(self.current_apt_id)
        finally:
            db.close()

        if success:
            messagebox.showinfo("Deleted", "Apartment removed from system.")
            from ui.apartments.apartment_list_page import ApartmentListPage
            self.controller.load_page(ApartmentListPage)
        else:
            messagebox.showerror("Error", "Could not delete from database.")