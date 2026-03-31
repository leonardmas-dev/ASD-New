import tkinter as tk
from tkinter import ttk

from backend.report_service import ReportService
from database.session import get_session


class FinancialReportPage(tk.Frame):
    """Shows total rent due, total paid, outstanding, and late fees."""

    def __init__(self, parent, main_window):
        super().__init__(parent)

        tk.Label(self, text="Financial Report", font=("Arial", 22)).pack(pady=20)

        db = get_session()
        service = ReportService(db)
        data = service.get_financial_summary()
        db.close()

        frame = tk.Frame(self)
        frame.pack(pady=10)

        rows = [
            ("Total Rent Due", f"£{data['total_due']}"),
            ("Total Rent Paid", f"£{data['total_paid']}"),
            ("Outstanding Balance", f"£{data['outstanding']}"),
            ("Total Late Fees", f"£{data['late_fees']}"),
        ]

        for label, value in rows:
            row = tk.Frame(frame)
            row.pack(anchor="w", pady=3)
            tk.Label(row, text=f"{label}: ", font=("Arial", 12, "bold")).pack(side="left")
            tk.Label(row, text=value, font=("Arial", 12)).pack(side="left")