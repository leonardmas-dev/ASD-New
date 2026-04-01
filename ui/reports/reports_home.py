import tkinter as tk


class ReportsHome(tk.Frame):
    """Staff reports menu."""

    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Reports", font=("Arial", 22)).pack(pady=20)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="Financial Report",
            width=25,
            command=self.open_financial_report
        ).grid(row=0, column=0, padx=5, pady=5)

        tk.Button(
            btn_frame,
            text="Maintenance Report",
            width=25,
            command=self.open_maintenance_report
        ).grid(row=1, column=0, padx=5, pady=5)

        tk.Button(
            btn_frame,
            text="Occupancy Report",
            width=25,
            command=self.open_occupancy_report
        ).grid(row=2, column=0, padx=5, pady=5)

    def open_financial_report(self):
        from ui.reports.financial_report_page import FinancialReportPage
        self.main_window.load_page(FinancialReportPage)

    def open_maintenance_report(self):
        from ui.reports.maintenance_report_page import MaintenanceReportPage
        self.main_window.load_page(MaintenanceReportPage)

    def open_occupancy_report(self):
        from ui.reports.occupancy_report_page import OccupancyReportPage
        self.main_window.load_page(OccupancyReportPage)