import tkinter as tk
from tkinter import ttk

from backend.report_service import ReportService
from database.session import get_session


class OccupancyReportPage(tk.Frame):
    """Shows occupancy rates and vacant apartments."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Occupancy Report", font=("Arial", 22)).pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Refresh", width=12, command=self.refresh).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Back", width=12, command=self.go_back).grid(row=0, column=1, padx=5)

        self.data_frame = tk.Frame(self)
        self.data_frame.pack(pady=15)

        self.load_data()

    def load_data(self):
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        db = get_session()
        service = ReportService(db)
        data = service.get_occupancy_summary()
        db.close()

        rows = [
            ("Total Apartments", data["total_apartments"]),
            ("Occupied Apartments", data["occupied"]),
            ("Vacant Apartments", data["vacant"]),
            ("Occupancy Rate", f"{data['occupancy_rate']}%"),
        ]

        for label, value in rows:
            row = tk.Frame(self.data_frame)
            row.pack(anchor="w", pady=3)
            tk.Label(row, text=f"{label}: ", font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(row, text=value, font=("Arial", 12)).pack(side="left")

    def refresh(self):
        self.load_data()

    def go_back(self):
        from ui.reports.reports_home import ReportsHome
        self.main_window.load_page(ReportsHome)