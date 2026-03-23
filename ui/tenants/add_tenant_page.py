import tkinter as tk
from tkinter import messagebox

def add_tenant():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    apartment = entry_apartment.get().strip()
    phone = entry_phone.get().strip()

    # Error Validation, if all fields not filled
    if not name or not age or not apartment:
        messagebox.showwarning("Please fill in all required fields.")
        return
    

    if not age.isdigit():
        messagebox.showwarning("Input Error", "Age must be a number.")
        return

    tenant_info = f"Name: {name}, Age: {age}, Apartment: {apartment}, Phone: {phone}"

    print(tenant_info)

    messagebox.showinfo("Tenant added successfully!")

    # Clear fields
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_apartment.delete(0, tk.END)
    entry_phone.delete(0, tk.END)

# Create base tkinter window
root = tk.Tk()
root.title("PAMS - Add Tenant")
root.geometry("400x500")

# Table of inputs for tenant info
tk.Label(root, text="Tenant Name *").pack(pady=5)
entry_name = tk.Entry(root, width=30)
entry_name.pack()

tk.Label(root, text="Age *").pack(pady=5)
entry_age = tk.Entry(root, width=30)
entry_age.pack()

tk.Label(root, text="Apartment Number *").pack(pady=5)
entry_apartment = tk.Entry(root, width=30)
entry_apartment.pack()

tk.Label(root, text="Phone Number").pack(pady=5)
entry_phone = tk.Entry(root, width=30)
entry_phone.pack()

tk.Label(root, text="*: Required Fields", fg="red", font=("Helvetica", 9)).pack(pady=5)


#submit btn will run add_tenant function
submit_btn = tk.Button(root,
            text="Add Tenant",
            width=20,
            command=add_tenant,
            bg="green",
            fg="black",
            activebackground="black",
            activeforeground="white")

submit_btn.pack(pady=20)

root.mainloop()