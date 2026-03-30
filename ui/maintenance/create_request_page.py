import tkinter as tk
from tkinter import ttk, messagebox
from database.session import SessionLocal
from backend.maintenance_service import MaintenanceService


class CreateMaintenanceRequestPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller  # main_window

        tk.Label(self, text="Create Maintenance Request", font=("Arial", 18, "bold")).pack(pady=20)

        form = tk.Frame(self)
        form.pack(pady=10)

        # tenant id
        tk.Label(form, text="Tenant ID:").grid(row=0, column=0, sticky="e", padx=10, pady=5)
        self.tenant_entry = tk.Entry(form)
        self.tenant_entry.grid(row=0, column=1, padx=10, pady=5)

        # apartment id
        tk.Label(form, text="Apartment ID:").grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.apartment_entry = tk.Entry(form)
        self.apartment_entry.grid(row=1, column=1, padx=10, pady=5)

        # category
        tk.Label(form, text="Category:").grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.category_cb = ttk.Combobox(form, values=["Plumbing", "Electrical", "Heating", "General"])
        self.category_cb.set("General")
        self.category_cb.grid(row=2, column=1, padx=10, pady=5)

        # priority
        tk.Label(form, text="Priority:").grid(row=3, column=0, sticky="e", padx=10, pady=5)
        self.priority_cb = ttk.Combobox(form, values=["Low", "Medium", "High"])
        self.priority_cb.set("Medium")
        self.priority_cb.grid(row=3, column=1, padx=10, pady=5)

        # description
        tk.Label(form, text="Description:").grid(row=4, column=0, sticky="ne", padx=10, pady=5)
        self.desc_text = tk.Text(form, width=40, height=5)
        self.desc_text.grid(row=4, column=1, padx=10, pady=5)

        btns = tk.Frame(self)
        btns.pack(pady=20)

        tk.Button(
            btns,
            text="Submit Request",
            bg="green",
            fg="white",
            width=18,
            command=self.submit_request,
        ).pack(side="left", padx=10)

        from ui.maintenance.maintenance_list_page import MaintenanceListPage
        tk.Button(
            btns,
            text="Back",
            width=12,
            command=lambda: self.controller.load_page(MaintenanceListPage),
        ).pack(side="left", padx=10)

    def submit_request(self):
        tenant_id = self.tenant_entry.get()
        apt_id = self.apartment_entry.get()
        category = self.category_cb.get()
        priority = self.priority_cb.get()
        description = self.desc_text.get("1.0", tk.END).strip()

        if not tenant_id or not apt_id or not description:
            messagebox.showerror("Error", "Tenant, Apartment, and Description are required.")
            return

        db = SessionLocal()
        service = MaintenanceService(db)
        try:
            ok = service.create_request(
                int(tenant_id),
                int(apt_id),
                category,
                description,
                priority,
                created_by_staff=True,
            )
        finally:
            db.close()

        if ok:
            messagebox.showinfo("Success", "Maintenance request created.")
            from ui.maintenance.maintenance_list_page import MaintenanceListPage
            self.controller.load_page(MaintenanceListPage)
        else:
            messagebox.showerror("Error", "Failed to create request.")