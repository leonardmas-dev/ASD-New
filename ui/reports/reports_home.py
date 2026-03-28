import tkinter as tk

class ReportsHomePage(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Reports", font=("Arial", 18, "bold")).pack(pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        from ui.reports.occupancy_report_page import OccupancyReportPage
        from ui.reports.financial_report_page import FinancialReportPage
        from ui.reports.maintenance_report_page import MaintenanceReportPage

        tk.Button(btn_frame, text="Occupancy Report", width=25,
                  command=lambda: main_window.load_page(OccupancyReportPage)).pack(pady=5)

        tk.Button(btn_frame, text="Financial Report", width=25,
                  command=lambda: main_window.load_page(FinancialReportPage)).pack(pady=5)

        tk.Button(btn_frame, text="Maintenance Report", width=25,
                  command=lambda: main_window.load_page(MaintenanceReportPage)).pack(pady=5)