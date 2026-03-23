import sys
import os
# Ensures database.models can be read by this file
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import tkinter as tk
from tkinter import ttk, messagebox
from database.models import Tenant
from database.session import get_session

#automatically close the session by using with
def fetch_tenants():
    with get_session() as session:
        tenants = session.query(Tenant).all()
    return tenants


root = tk.Tk()
root.title("Tenant List")
root.geometry("1200x400")

tk.Label(root, text="Tenant Information")

# Displaying the tenant data
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