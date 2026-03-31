import tkinter as tk
from tkinter import ttk

from backend.report_service import ReportService
from database.session import get_session


class MaintenanceReportPage(tk.Frame):
    """Shows maintenance statistics."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Maintenance Report", font=("Arial", 22)).pack(pady=20)

        db = get_session()
        service = ReportService(db)
        data = service.get_maintenance_summary()
        db.close()

        frame = tk.Frame(self)
        frame.pack(pady=10)

        rows = [
            ("Total Requests", data["total_requests"]),
            ("Completed Requests", data["completed"]),
            ("Pending Requests", data["pending"]),
            ("Average Completion Time (hrs)", data["avg_time"]),
            ("Total Maintenance Cost", f"£{data['total_cost']}"),
        ]

        for label, value in rows:
            row = tk.Frame(frame)
            row.pack(anchor="w", pady=3)
            tk.Label(row, text=f"{label}: ", font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(row, text=value, font=("Arial", 12)).pack(side="left")