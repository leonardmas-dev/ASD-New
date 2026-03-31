import tkinter as tk
from tkinter import ttk

from backend.report_service import ReportService
from database.session import get_session


class OccupancyReportPage(tk.Frame):
    """Shows occupancy rates and vacant apartments."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Occupancy Report", font=("Arial", 22)).pack(pady=20)

        db = get_session()
        service = ReportService(db)
        data = service.get_occupancy_summary()
        db.close()

        frame = tk.Frame(self)
        frame.pack(pady=10)

        rows = [
            ("Total Apartments", data["total_apartments"]),
            ("Occupied Apartments", data["occupied"]),
            ("Vacant Apartments", data["vacant"]),
            ("Occupancy Rate", f"{data['occupancy_rate']}%"),
        ]

        for label, value in rows:
            row = tk.Frame(frame)
            row.pack(anchor="w", pady=3)
            tk.Label(row, text=f"{label}: ", font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(row, text=value, font=("Arial", 12)).pack(side="left")