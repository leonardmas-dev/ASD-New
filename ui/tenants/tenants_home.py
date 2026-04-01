import tkinter as tk
from tkinter import ttk

from database.session import get_session
from database.models import Tenant


class TenantsHome(tk.Frame):
    """Staff overview of all tenants."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Tenants", font=("Arial", 22)).pack(pady=20)

        # buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Add Tenant",
            width=18,
            command=self.open_add_page
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Edit Tenant",
            width=18,
            command=self.open_edit_page
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            btn_frame,
            text="View Tenant List",
            width=18,
            command=self.open_list_page
        ).grid(row=0, column=2, padx=5)

        # table
        self.table = ttk.Treeview(
            self,
            columns=("id", "name", "email", "phone", "active"),
            show="headings",
        )

        for col, text in [
            ("id", "ID"),
            ("name", "Name"),
            ("email", "Email"),
            ("phone", "Phone"),
            ("active", "Active"),
        ]:
            self.table.heading(col, text=text)

        self.table.pack(fill="both", expand=True, pady=10)

        self.load_data()

    # load tenants
    def load_data(self):
        db = get_session()
        tenants = db.query(Tenant).all()

        # extract before closing session
        tenant_rows = []
        for t in tenants:
            tenant_rows.append((
                t.tenant_id,
                f"{t.first_name} {t.last_name}",
                t.email,
                t.phone,
                "Yes" if t.is_active else "No",
            ))

        db.close()

        for row in tenant_rows:
            self.table.insert("", "end", values=row)

    # open add tenant page
    def open_add_page(self):
        from ui.tenants.add_tenant_page import AddTenantPage
        self.main_window.load_page(AddTenantPage)

    # open edit tenant page
    def open_edit_page(self):
        selected = self.table.selection()
        if not selected:
            return  # or show a messagebox if you want
        tenant_id = self.table.item(selected[0], "values")[0]
        from ui.tenants.edit_tenant_page import EditTenantPage
        self.main_window.load_page(EditTenantPage, tenant_id)

    # open tenant list page
    def open_list_page(self):
        from ui.tenants.tenant_list_page import TenantListPage
        self.main_window.load_page(TenantListPage)