import tkinter as tk
from tkinter import ttk, messagebox
from backend.user_service import UserService
from database.session import get_session
from database.models import Location


class EditUserPage(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window
        self.current_user_id = None  # updates when a row is selected

        tk.Label(self, text="Edit User", font=("Arial", 18, "bold")).pack(pady=10)

        # table container
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, pady=10)

        # user table
        self.table = ttk.Treeview(
            table_frame,
            columns=("id", "name", "role", "location", "status"),
            show="headings",
            height=8,
            selectmode="browse"  # ensure row selection works
        )

        self.table.heading("id", text="ID")
        self.table.heading("name", text="Name")
        self.table.heading("role", text="Role")
        self.table.heading("location", text="Location")
        self.table.heading("status", text="Status")

        self.table.column("id", width=50)

        self.table.pack(fill="both", expand=True)

        # row selection handlers
        self.table.bind("<<TreeviewSelect>>", self.on_row_select)
        self.table.bind("<ButtonRelease-1>", self.on_row_click)

        self.load_users()

        # form fields
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

        tk.Label(form, text="New Password").grid(row=4, column=0, sticky="w")
        self.password = tk.Entry(form, show="*")
        self.password.grid(row=4, column=1, pady=5)

        tk.Label(form, text="Role").grid(row=5, column=0, sticky="w")
        self.role_box = ttk.Combobox(
            form,
            values=["admin", "manager", "frontdesk", "finance", "maintenance"]
        )
        self.role_box.grid(row=5, column=1, pady=5)

        tk.Label(form, text="Location").grid(row=6, column=0, sticky="w")
        self.location_box = ttk.Combobox(form)
        self.location_box.grid(row=6, column=1, pady=5)

        self.load_locations()

        # action buttons
        tk.Button(self, text="Save Changes", command=self.save_user, width=20).pack(pady=10)
        tk.Button(self, text="Deactivate User", command=self.deactivate_user).pack(pady=5)
        tk.Button(self, text="Activate User", command=self.activate_user).pack(pady=5)

        from ui.user_management.users_home import UsersHomePage
        tk.Button(self, text="Back", command=lambda: main_window.load_page(UsersHomePage)).pack(pady=10)

    # populate table
    def load_users(self):
        for row in self.table.get_children():
            self.table.delete(row)

        users = UserService.get_all_users()

        for u in users:
            name = f"{u.first_name} {u.last_name}"
            status = "Active" if u.is_active else "Inactive"
            location = u.location.city if u.location else "N/A"

            self.table.insert(
                "",
                "end",
                values=(u.user_id, name, u.role, location, status),
                iid=u.user_id
            )

    # populate location dropdown
    def load_locations(self):
        db = get_session()
        locations = db.query(Location).all()
        db.close()
        self.location_box["values"] = [f"{loc.location_id} - {loc.city}" for loc in locations]

    # ensure row selection triggers correctly
    def on_row_click(self, event):
        row = self.table.identify_row(event.y)
        if row:
            self.table.selection_set(row)
            self.on_row_select(None)

    # row selection handler
    def on_row_select(self, event):
        selected = self.table.selection()
        if not selected:
            return

        user_id = int(selected[0])
        self.load_user(user_id)

    # load user into fields
    def load_user(self, user_id):
        self.current_user_id = user_id
        user = UserService.get_user_by_id(user_id)

        # reset fields
        self.first_name.delete(0, tk.END)
        self.last_name.delete(0, tk.END)
        self.email.delete(0, tk.END)
        self.phone.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.role_box.set("")
        self.location_box.set("")

        # populate fields
        self.first_name.insert(0, user.first_name)
        self.last_name.insert(0, user.last_name)
        self.email.insert(0, user.email)
        self.phone.insert(0, user.phone)
        self.role_box.set(user.role)

        if user.location:
            self.location_box.set(f"{user.location_id} - {user.location.city}")

    # commit changes
    def save_user(self):
        if not self.current_user_id:
            return

        loc_id = int(self.location_box.get().split(" - ")[0])

        data = {
            "first_name": self.first_name.get(),
            "last_name": self.last_name.get(),
            "email": self.email.get(),
            "phone": self.phone.get(),
            "role": self.role_box.get(),
            "location_id": loc_id,
            "password": self.password.get() if self.password.get() else None
        }

        UserService.update_user(self.current_user_id, data)
        messagebox.showinfo("Success", "User updated.")

    def deactivate_user(self):
        if self.current_user_id:
            UserService.deactivate_user(self.current_user_id)
            messagebox.showinfo("Success", "User deactivated.")

    def activate_user(self):
        if self.current_user_id:
            UserService.activate_user(self.current_user_id)
            messagebox.showinfo("Success", "User activated.")