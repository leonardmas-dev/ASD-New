import tkinter as tk
from tkinter import ttk, messagebox

from backend.tenant_service import TenantService
from database.session import get_session
from database.models import TenantAccount, Location
import bcrypt


class EditTenantPage(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.current_tenant_id = None

        tk.Label(self, text="Edit Tenant", font=("Arial", 18, "bold")).pack(pady=10)

        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10)

        self.table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "phone", "email", "location", "status"),
            show="headings",
            height=8,
            selectmode="browse"
        )

        self.table.heading("id", text="ID")
        self.table.heading("name", text="Name")
        self.table.heading("phone", text="Phone")
        self.table.heading("email", text="Email")
        self.table.heading("location", text="Location")
        self.table.heading("status", text="Status")

        self.table.column("id", width=50)

        self.table.pack(fill="both", expand=True)

        self.table.bind("<<TreeviewSelect>>", self.on_row_select)
        self.table.bind("<ButtonRelease-1>", self.on_row_click)

        self.load_tenants()

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="First Name").grid(row=0, column=0, sticky="w")
        self.first_name = tk.Entry(form)
        self.first_name.grid(row=0, column=1, pady=5)

        tk.Label(form, text="Last Name").grid(row=1, column=0, sticky="w")
        self.last_name = tk.Entry(form)
        self.last_name.grid(row=1, column=1, pady=5)

        tk.Label(form, text="Email").grid(row=2, column=0, sticky="w")
        self.email = tk.Entry(form)
        self.email.grid(row=2, column=1, pady=5)

        tk.Label(form, text="Phone").grid(row=3, column=0, sticky="w")
        self.phone = tk.Entry(form)
        self.phone.grid(row=3, column=1, pady=5)

        tk.Label(form, text="Occupation").grid(row=4, column=0, sticky="w")
        self.occupation = tk.Entry(form)
        self.occupation.grid(row=4, column=1, pady=5)

        tk.Label(form, text="New Password").grid(row=5, column=0, sticky="w")
        self.password = tk.Entry(form, show="*")
        self.password.grid(row=5, column=1, pady=5)

        tk.Label(form, text="Location").grid(row=6, column=0, sticky="w")
        self.location_box = ttk.Combobox(form)
        self.location_box.grid(row=6, column=1, pady=5)

        self.load_locations()

        tk.Button(self, text="Save Changes", command=self.save_tenant, width=20).pack(pady=10)
        tk.Button(self, text="Deactivate Tenant", command=self.deactivate_tenant).pack(pady=5)
        tk.Button(self, text="Activate Tenant", command=self.activate_tenant).pack(pady=5)

        tk.Button(self, text="Back", command=self.go_back).pack(pady=10)

    def load_tenants(self):
        for row in self.table.get_children():
            self.table.delete(row)

        tenants = TenantService.get_all_tenants()

        for t in tenants:
            name = f"{t.first_name} {t.last_name}"
            status = "Active" if t.is_active else "Inactive"
            location = t.location.city if t.location else "N/A"

            self.table.insert(
                "",
                "end",
                values=(t.tenant_id, name, t.phone, t.email, location, status),
                iid=t.tenant_id
            )

    def load_locations(self):
        db = get_session()
        locations = db.query(Location).all()
        db.close()
        self.location_box["values"] = [f"{loc.location_id} - {loc.city}" for loc in locations]

    def on_row_click(self, event):
        row = self.table.identify_row(event.y)
        if row:
            self.table.selection_set(row)
            self.on_row_select(None)

    def on_row_select(self, event):
        selected = self.table.selection()
        if not selected:
            return

        tenant_id = int(selected[0])
        self.load_tenant(tenant_id)

    def load_tenant(self, tenant_id):
        self.current_tenant_id = tenant_id
        tenant = TenantService.get_tenant_by_id(tenant_id)

        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.occupation.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.location_box.set("")

        self.first_name.insert(0, tenant.first_name)
        self.last_name.insert(0, tenant.last_name)
        self.email.insert(0, tenant.email)
        self.phone.insert(0, tenant.phone)
        self.occupation.insert(0, tenant.occupation if tenant.occupation else "")

        if tenant.location:
            self.location_box.set(f"{tenant.location_id} - {tenant.location.city}")

    def save_tenant(self):
        if not self.current_tenant_id:
            return

        loc_id = int(self.location_box.get().split(" - ")[0])

        tenant = TenantService.get_tenant_by_id(self.current_tenant_id)

        data = {
            "first_name": self.first_name.get(),
            "last_name": self.last_name.get(),
            "email": self.email.get(),
            "phone": self.phone.get(),
            "ni_number": tenant.ni_number,
            "occupation": self.occupation.get(),
            "location_id": loc_id,
        }

        TenantService.update_tenant(self.current_tenant_id, data)

        if self.password.get().strip():
            db = get_session()
            account = db.query(TenantAccount).filter(TenantAccount.tenant_id == self.current_tenant_id).first()
            if account:
                hashed_pw = bcrypt.hashpw(
                    self.password.get().encode("utf-8"),
                    bcrypt.gensalt()
                ).decode("utf-8")
                account.password_hash = hashed_pw
                db.commit()
            db.close()

        messagebox.showinfo("Success", "Tenant updated.")
        self.load_tenants()

    def deactivate_tenant(self):
        if self.current_tenant_id:
            TenantService.deactivate_tenant(self.current_tenant_id)
            messagebox.showinfo("Success", "Tenant deactivated.")
            self.load_tenants()

    def activate_tenant(self):
        if self.current_tenant_id:
            TenantService.activate_tenant(self.current_tenant_id)
            messagebox.showinfo("Success", "Tenant activated.")
            self.load_tenants()

    def go_back(self):
        from ui.tenants.tenants_home import TenantsHome
        self.main_window.load_page(TenantsHome)