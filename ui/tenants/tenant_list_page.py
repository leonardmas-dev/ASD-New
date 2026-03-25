
import tkinter as tk
from tkinter import ttk, messagebox
from backend.tenant_service import fetch_tenants
from database.models import Tenant
from database.session import get_session
from tenants_home import TenantsHome


'''
#automatically close the session by using with
def fetch_tenants():
    with get_session() as session:
        tenants = session.query(Tenant).all()
    return tenants


root = tk.Tk()
root.title("Tenant List")
root.geometry("1200x400")

tk.Label(root, text="Tenant Information")

# Displaying the tenant data in tkinter tree
columns = ("Tenant ID", "First Name", "Last Name", "Phone", "Email", "Apartment")
tree = ttk.Treeview(root, columns=columns, show="headings")



for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)

tree.pack(fill="both", expand=True)


# If content goes off screen scroll bar allows to view more
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Fetch tenants and insert into treeview
for tenant in fetch_tenants():
    tree.insert(
        "",
        "end",
        values=(
            tenant.tenant_id,
            tenant.first_name,
            tenant.last_name,
            tenant.phone,
            tenant.email,
            tenant.location_id 
        )
    )


def delete_tenant():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showwarning("Warning", "Select the tenant you want to delete first")
        return

    


    tenant_data = tree.item(selected_item)["values"]
    tenant_id = tenant_data[0]
    #tenant_data is [1] and [2] because of how its displayed in the ui not in the database as first_name and last_name are the 2nd and 3rd items in the tree.
    tenant_fname = tenant_data[1]
    tenant_lname = tenant_data[2]
    tenant_fullname = tenant_fname + " " + tenant_lname


    confirm = messagebox.askyesno("Confirm", f"Delete {tenant_fullname} tenant?")
    if not confirm:
        return
    
    messagebox.showwarning("Tenant Deleted", f"{tenant_fullname}, was deleted.")

    # Delete from database
    with get_session() as session:
        tenant = session.query(Tenant).filter_by(tenant_id=tenant_id).first()
        if tenant:
            session.delete(tenant)
            session.commit()



    # Remove from table in real time
    tree.delete(selected_item)




delete_btn = tk.Button(root, text="Delete Tenant", command=delete_tenant)
delete_btn.pack(pady=10)

root.mainloop()

'''


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

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.load_data()

        # Delete Tenant button wont work unless a tenant_id is selected
        delete_btn = tk.Button(self, text="Delete Tenant", command=self.delete_tenant)
        delete_btn.pack(pady=10)

        go_homebtn = tk.Button(self, text="Go Home", command=lambda: main_window.load_page(TenantsHome))
        go_homebtn.pack(pady=10)


    def load_data(self):
        for tenant in fetch_tenants():
            self.tree.insert("", "end", values=(
                tenant.tenant_id,
                tenant.first_name,
                tenant.last_name,
                tenant.phone,
                tenant.email,
                tenant.location_id
            ))

    def delete_tenant(self):
        selected_item = self.tree.selection()


        if not selected_item:
            messagebox.showwarning("Warning", "Select a tenant first")
            return

        tenant_data = self.tree.item(selected_item)["values"]
        tenant_id = tenant_data[0]



        with get_session() as session:
            tenant = session.query(Tenant).filter_by(tenant_id=tenant_id).first()
            if tenant:
                session.delete(tenant)
                session.commit()

        self.tree.delete(selected_item)