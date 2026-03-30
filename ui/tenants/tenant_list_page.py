import tkinter as tk
from tkinter import ttk, messagebox
from backend.tenant_service import fetch_tenants
from database.models import Tenant
from database.session import get_session
from ui.tenants.tenants_home import TenantsHome



class TenantList(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        tenant_list_title = tk.Label(self, text="Tenant Information")
        tenant_list_title.pack()

        columns = ("Tenant ID", "First Name", "Last Name", "Phone", "Email", "Apartment")
        self.tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True)


        # If content goes off screen scroll bar allows to view more
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_data()

        # Delete Tenant button wont work unless a tenant_id is selected
        delete_btn = tk.Button(self, text="Delete Tenant", command=self.delete_tenant)
        delete_btn.pack(pady=10)

        go_homebtn = tk.Button(self, text="Go Home", command=lambda: main_window.load_page(TenantsHome))
        go_homebtn.pack(pady=10)

    # Fetch tenants and insert into treeview
    def load_data(self):
        for tenant in fetch_tenants():
            self.tree.insert("", "end", values=(
                tenant.tenant_id,
                tenant.first_name,
                tenant.last_name,
                tenant.phone,
                tenant.email,
                #tenant.is_active
                tenant.location_id
            ))

    def delete_tenant(self):
        selected_item = self.tree.selection()

        # Tenant wont 
        if not selected_item:
            messagebox.showwarning("Warning", "Select a tenant first")
            return

        tenant_data = self.tree.item(selected_item)["values"]
        tenant_id = tenant_data[0]


        #automatically close the session by using with
        with get_session() as session:
            tenant = session.query(Tenant).filter_by(tenant_id=tenant_id).first()
            if tenant:
                session.delete(tenant)
                session.commit()


        # Remove the tenant from list on tkinter page 
        self.tree.delete(selected_item)