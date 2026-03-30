import tkinter as tk
from tkinter import ttk, messagebox

from database.session import SessionLocal
from backend.maintenance_service import MaintenanceService


class MaintenanceListPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Maintenance Requests", font=("Arial", 18, "bold")).pack(pady=20)

        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        cols = ("id", "tenant", "apt", "category", "priority", "status", "created")
        self.tree = ttk.Treeview(table_frame, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c.capitalize())

        self.tree.column("id", width=50)
        self.tree.column("tenant", width=150)
        self.tree.column("apt", width=150)
        self.tree.column("category", width=120)
        self.tree.column("priority", width=80)
        self.tree.column("status", width=100)
        self.tree.column("created", width=150)

        self.tree.pack(fill="both", expand=True)

        btns = tk.Frame(self)
        btns.pack(pady=10)

        tk.Button(btns, text="Refresh", width=12, command=self.load_data).pack(side="left", padx=10)

        tk.Button(
            btns,
            text="Update Request",
            bg="#3498db",
            fg="white",
            width=15,
            command=self.open_update,
        ).pack(side="left", padx=10)

        from ui.maintenance.create_request_page import CreateMaintenanceRequestPage
        tk.Button(
            btns,
            text="New Request",
            bg="green",
            fg="white",
            width=15,
            command=lambda: self.controller.load_page(CreateMaintenanceRequestPage),
        ).pack(side="left", padx=10)

        self.load_data()

    def load_data(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        db = SessionLocal()
        service = MaintenanceService(db)
        try:
            rows = service.get_all_requests()
        finally:
            db.close()

        for r in rows:
            self.tree.insert(
                "",
                "end",
                values=(
                    r["request_id"],
                    r["tenant_name"],
                    r["apartment_label"],
                    r["category"],
                    r["priority"],
                    r["status"],
                    r["created_at"],
                ),
            )

    def open_update(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Select", "Choose a request to update.")
            return

        data = self.tree.item(selected)["values"]

        from ui.maintenance.update_request_page import UpdateMaintenanceRequestPage
        self.controller.load_page(
            UpdateMaintenanceRequestPage,
            request_id=data[0],
            tenant_name=data[1],
            apt_label=data[2],
            category=data[3],
            priority=data[4],
            status=data[5],
        )