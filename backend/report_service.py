# Student: Yaseen Sassi     StudentID: 24023127

from sqlalchemy import func
from sqlalchemy.orm import joinedload

from database.session import get_session
from database.models import (
    Apartment,
    Lease,
    Payment,
    MaintenanceRequest,
    Location,
)


class ReportService:
    """Provides occupancy, financial, and maintenance summaries."""

    @staticmethod
    def get_occupancy_summary():
        """Return total apartments, occupied, vacant, and occupancy rate."""
        db = get_session()

        total = db.query(Apartment).filter(Apartment.is_active == True).count()

        occupied = (
            db.query(Lease)
            .filter(Lease.is_active == True)
            .count()
        )

        db.close()

        vacant = total - occupied
        rate = round((occupied / total) * 100, 2) if total > 0 else 0

        return {
            "total_apartments": total,
            "occupied": occupied,
            "vacant": vacant,
            "occupancy_rate": rate,
        }

    @staticmethod
    def get_financial_summary():
        """Return total rent due, total paid, outstanding, and late fees."""
        db = get_session()

        totals = (
            db.query(
                func.sum(Payment.amount_due).label("due"),
                func.sum(Payment.amount_paid).label("paid"),
                func.sum(Payment.late_fee).label("late_fees"),
            )
            .first()
        )

        db.close()

        total_due = totals.due or 0
        total_paid = totals.paid or 0
        late_fees = totals.late_fees or 0
        outstanding = total_due - total_paid

        return {
            "total_due": round(total_due, 2),
            "total_paid": round(total_paid, 2),
            "outstanding": round(outstanding, 2),
            "late_fees": round(late_fees, 2),
        }
    @staticmethod
    def get_maintenance_summary():
        db = get_session()

        total_requests = db.query(MaintenanceRequest).count()

        completed = (
            db.query(MaintenanceRequest)
            .filter(MaintenanceRequest.status == "Completed")
            .count()
        )

        pending = (
            db.query(MaintenanceRequest)
            .filter(MaintenanceRequest.status != "Completed")
            .count()
        )

        avg_time = (
            db.query(func.avg(MaintenanceRequest.time_taken_hours))
            .filter(MaintenanceRequest.time_taken_hours.isnot(None))
            .scalar()
        )

        total_cost = (
            db.query(func.sum(MaintenanceRequest.cost))
            .scalar()
        )

        db.close()

        return {
            "total_requests": total_requests,
            "completed": completed,
            "pending": pending,
            "avg_time": round(avg_time, 2) if avg_time else 0,
            "total_cost": round(total_cost, 2) if total_cost else 0,
        }

    # occupancy Table
    @staticmethod
    def get_occupancy_report(city=None):
        """Return detailed occupancy per apartment."""
        db = get_session()

        query = (
            db.query(Apartment)
            .options(
                joinedload(Apartment.location),
                joinedload(Apartment.leases).joinedload(Lease.tenant),
            )
            .filter(Apartment.is_active == True)
        )

        if city:
            query = query.join(Apartment.location).filter(Location.city == city)

        apartments = query.all()
        db.close()

        rows = []
        for apt in apartments:
            loc = apt.location.city

            active_lease = next((l for l in apt.leases if l.is_active), None)

            if active_lease:
                tenant = active_lease.tenant
                tenant_name = f"{tenant.first_name} {tenant.last_name}"
                status = "Occupied"
            else:
                tenant_name = "-"
                status = "Vacant"

            rows.append(
                {
                    "apartment_id": apt.apartment_id,
                    "city": loc,
                    "status": status,
                    "tenant": tenant_name,
                    "rent": apt.monthly_rent,
                }
            )

        return rows
    # finance table
    @staticmethod
    def get_financial_report(city=None):
        """Return detailed financial rows per apartment."""
        db = get_session()

        query = (
            db.query(
                Apartment.apartment_id,
                Location.city,
                func.sum(Payment.amount_paid).label("collected"),
                func.sum(Payment.amount_due).label("expected"),
            )
            .join(Apartment.location)
            .join(Lease, Lease.apartment_id == Apartment.apartment_id)
            .join(Payment, Payment.lease_id == Lease.lease_id)
            .group_by(Apartment.apartment_id, Location.city)
        )

        if city:
            query = query.filter(Location.city == city)

        results = query.all()
        db.close()

        rows = []
        for apt_id, city_name, collected, expected in results:
            collected = collected or 0
            expected = expected or 0
            pending = expected - collected

            rows.append(
                {
                    "apartment_id": apt_id,
                    "city": city_name,
                    "collected": round(collected, 2),
                    "expected": round(expected, 2),
                    "pending": round(pending, 2),
                }
            )

        return rows

    # maintenance Table
    @staticmethod
    def get_maintenance_report(city=None):
        """Return detailed maintenance cost rows per apartment."""
        db = get_session()

        query = (
            db.query(
                Apartment.apartment_id,
                Location.city,
                func.sum(MaintenanceRequest.cost).label("total_cost"),
                func.count(MaintenanceRequest.maintenance_request_id).label("count"),
            )
            .join(Apartment.location)
            .join(MaintenanceRequest, MaintenanceRequest.apartment_id == Apartment.apartment_id)
            .group_by(Apartment.apartment_id, Location.city)
        )

        if city:
            query = query.filter(Location.city == city)

        results = query.all()
        db.close()

        rows = []
        for apt_id, city_name, total_cost, count in results:
            rows.append(
                {
                    "apartment_id": apt_id,
                    "city": city_name,
                    "total_cost": round(total_cost or 0, 2),
                    "count": count,
                }
            )

        return rows