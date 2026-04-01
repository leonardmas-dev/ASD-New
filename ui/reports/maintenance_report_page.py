import tkinter as tk
from tkinter import ttk

from backend.report_service import ReportService


class MaintenanceReportPage(tk.Frame):
    """Shows maintenance statistics."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Maintenance Cost Report", font=("Arial", 22)).pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        tk.Button(
            btn_frame,
            text="Refresh",
            width=12,
            command=self.refresh,
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            btn_frame,
            text="Back",
            width=12,
            command=self.go_back,
        ).grid(row=0, column=1, padx=5)

        self.data_frame = tk.Frame(self)
        self.data_frame.pack(pady=15)

        self.load_data()

    def load_data(self):
        for widget in self.data_frame.winfo_children():
            widget.destroy()

        data = ReportService.get_maintenance_summary()

        rows = [
            ("Total Requests", data["total_requests"]),
            ("Completed Requests", data["completed"]),
            ("Pending Requests", data["pending"]),
            ("Average Completion Time (hrs)", data["avg_time"]),
            ("Total Maintenance Cost", f"£{data['total_cost']}"),
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
        self.main_window.load_page(lambda parent, mw: ReportsHome(parent, mw))