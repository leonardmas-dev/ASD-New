import tkinter as tk
from tkinter import ttk, messagebox

from backend.maintenance_service import MaintenanceService
from database.session import get_session


class UpdateRequestPage(tk.Frame):
    """Staff updates an existing maintenance request."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        self.main_window = main_window
        self.current_request_id = None

        tk.Label(self, text="Update Maintenance Request", font=("Arial", 22)).pack(pady=20)

        select_frame = tk.Frame(self)
        select_frame.pack(pady=5)

        tk.Label(select_frame, text="Select Request:").grid(row=0, column=0, sticky="e")
        self.request_combo = ttk.Combobox(select_frame, state="readonly", width=45)
        self.request_combo.grid(row=0, column=1, padx=5, pady=5)
        self.request_combo.bind("<<ComboboxSelected>>", self.on_request_selected)

        form = tk.Frame(self)
        form.pack(pady=10)

        tk.Label(form, text="Status:").grid(row=0, column=0, sticky="e")
        self.status_combo = ttk.Combobox(
            form,
            values=["Pending", "Scheduled", "In Progress", "Completed"],
            state="readonly",
            width=20,
        )
        self.status_combo.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Time Taken (hours):").grid(row=1, column=0, sticky="e")
        self.time_entry = tk.Entry(form, width=20)
        self.time_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Cost (£):").grid(row=2, column=0, sticky="e")
        self.cost_entry = tk.Entry(form, width=20)
        self.cost_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(form, text="Notes:").grid(row=3, column=0, sticky="e")
        self.notes_entry = tk.Entry(form, width=45)
        self.notes_entry.grid(row=3, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Save Changes", command=self.save, width=18).grid(
            row=0, column=0, padx=5
        )
        tk.Button(btn_frame, text="Back", command=self.go_back, width=10).grid(
            row=0, column=1, padx=5
        )

        self._load_requests()

    def _load_requests(self):
        db = get_session()
        service = MaintenanceService(db)
        rows = service.get_all_requests()
        db.close()

        self.request_map = {
            f"{r['request_id']} - {r['tenant_name']} - {r['apartment_label']} ({r['status']})":
                r["request_id"]
            for r in rows
        }

        self.request_combo["values"] = list(self.request_map.keys())

    def on_request_selected(self, event=None):
        label = self.request_combo.get()
        if not label:
            return

        self.current_request_id = self.request_map.get(label)
        if not self.current_request_id:
            return

        db = get_session()
        service = MaintenanceService(db)
        req = service.get_request_by_id(self.current_request_id)
        db.close()

        if not req:
            messagebox.showerror("Error", "Request not found.")
            return

        self.status_combo.set(req.get("status", ""))

        self.time_entry.delete(0, tk.END)
        if req.get("time_taken_hours") is not None:
            self.time_entry.insert(0, str(req["time_taken_hours"]))

        self.cost_entry.delete(0, tk.END)
        if req.get("cost") is not None:
            self.cost_entry.insert(0, str(req["cost"]))

        self.notes_entry.delete(0, tk.END)
        if req.get("notes"):
            self.notes_entry.insert(0, req["notes"])

    def save(self):
        if not self.current_request_id:
            messagebox.showerror("Error", "Select a request first.")
            return

        status = self.status_combo.get()
        time_taken_raw = self.time_entry.get().strip()
        cost_raw = self.cost_entry.get().strip()
        notes = self.notes_entry.get().strip()

        try:
            time_taken = float(time_taken_raw) if time_taken_raw else None
        except ValueError:
            messagebox.showerror("Error", "Time taken must be a number.")
            return

        try:
            cost = float(cost_raw) if cost_raw else None
        except ValueError:
            messagebox.showerror("Error", "Cost must be a number.")
            return

        db = get_session()
        service = MaintenanceService(db)
        ok = service.update_request(
            self.current_request_id,
            status,
            time_taken,
            cost,
            notes,
        )
        db.close()

        if ok:
            messagebox.showinfo("Success", "Request updated.")
        else:
            messagebox.showerror("Error", "Failed to update request.")

    def go_back(self):
        from ui.maintenance.maintenance_home import MaintenanceHome
        self.main_window.load_page(MaintenanceHome)