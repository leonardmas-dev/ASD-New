import tkinter as tk
from tkinter import ttk
from backend.report_service import ReportService


class FinancialReportPage(tk.Frame):
    def __init__(self, parent, main_window):
        super().__init__(parent)
        self.main_window = main_window

        tk.Label(self, text="Financial Report", font=("Arial", 18, "bold")).pack(pady=10)

        filter_frame = tk.Frame(self)
        filter_frame.pack(pady=5)

        tk.Label(filter_frame, text="City").grid(row=0, column=0)
        self.city_box = ttk.Combobox(filter_frame, width=20)
        self.city_box.grid(row=0, column=1, padx=5)
        self.city_box["values"] = ["All"] + ReportService.get_cities()
        self.city_box.set("All")

        tk.Button(filter_frame, text="Refresh", command=self.load_data).grid(row=0, column=2, padx=5)

        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True)

        self.table = ttk.Treeview(
            table_frame,
            columns=("apt", "city", "collected", "expected", "pending"),
            show="headings",
            height=12
        )

        self.table.heading("apt", text="Apartment ID")
        self.table.heading("city", text="City")
        self.table.heading("collected", text="Collected (£)")
        self.table.heading("expected", text="Expected (£)")
        self.table.heading("pending", text="Pending (£)")

        self.table.pack(fill="both", expand=True)

        from ui.reports.reports_home import ReportsHomePage
        tk.Button(self, text="Back", command=lambda: main_window.load_page(ReportsHomePage)).pack(pady=10)

        self.load_data()

    def load_data(self):
        for row in self.table.get_children():
            self.table.delete(row)

        city = self.city_box.get()
        rows = ReportService.get_financial_summary(None if city == "All" else city)

        for r in rows:
            self.table.insert("", "end", values=(
                r["apartment_id"], r["city"], r["collected"], r["expected"], r["pending"]
            ))