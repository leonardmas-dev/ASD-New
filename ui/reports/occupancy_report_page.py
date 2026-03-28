import tkinter as tk
from tkinter import ttk
from backend.report_service import ReportService


class OccupancyReportPage(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Occupancy Report", font=("Arial", 18, "bold")).pack(pady=10)

        # filter
        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="City").grid(row=0, column=0)
        self.city_box = ttk.Combobox(filter_frame, width=20)
        self.city_box.grid(row=0, column=1, padx=5)
        self.city_box["values"] = ["All"] + ReportService.get_cities()
        self.city_box.set("All")

        tk.Button(filter_frame, text="Refresh", command=self.load_data).grid(row=0, column=2, padx=5)

        # table
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        self.table = ttk.Treeview(
            table_frame,
            columns=("apt", "city", "status", "tenant", "rent"),
            show="headings",
            height=12
        )

        self.table.heading("apt", text="Apartment ID")
        self.table.heading("city", text="City")
        self.table.heading("status", text="Status")
        self.table.heading("tenant", text="Tenant")
        self.table.heading("rent", text="Rent (£)")

        self.table.pack(fill="both", expand=True)

        from ui.reports.reports_home import ReportsHomePage
        tk.Button(self, text="Back", command=lambda: main_window.load_page(ReportsHomePage)).pack(pady=10)

        self.load_data()

    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        city = self.city_box.get()
        rows = ReportService.get_occupancy_report(None if city == "All" else city)

        for r in rows:
            self.table.insert("", "end", values=(
                r["apartment_id"], r["city"], r["status"], r["tenant"], r["rent"]
            ))