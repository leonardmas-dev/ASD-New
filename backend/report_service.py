from sqlalchemy import func
from sqlalchemy.orm import joinedload
from database.session import get_session
from database.models import (
    Apartment, Lease, Payment, MaintenanceRequest, Location, Tenant
)


class ReportService:

    # List of cities for dropdown
    @staticmethod
    def get_cities():
        db = get_session()
        cities = db.query(Location.city).distinct().all()
        db.close()
        return [c[0] for c in cities]

    # OCCUPANCY REPORT

    @staticmethod
    def get_occupancy_report(city=None):
        db = get_session()

        query = (
            db.query(Apartment)
            .options(
                joinedload(Apartment.location),
                joinedload(Apartment.leases).joinedload(Lease.tenant)
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

            # find active lease
            active_lease = next((l for l in apt.leases if l.is_active), None)

            if active_lease:
                tenant = active_lease.tenant
                tenant_name = f"{tenant.first_name} {tenant.last_name}"
                status = "Occupied"
            else:
                tenant_name = "-"
                status = "Vacant"

            rows.append({
                "apartment_id": apt.apartment_id,
                "city": loc,
                "status": status,
                "tenant": tenant_name,
                "rent": apt.monthly_rent
            })

        return rows

    # FINANCIAL REPORT

    @staticmethod
    def get_financial_summary(city=None):
        db = get_session()

        query = (
            db.query(
                Apartment.apartment_id,
                Location.city,
                func.sum(Payment.amount_paid).label("collected"),
                func.sum(Payment.amount_due).label("expected")
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

            rows.append({
                "apartment_id": apt_id,
                "city": city_name,
                "collected": collected,
                "expected": expected,
                "pending": pending
            })

        return rows

    # MAINTENANCE COST REPORT

    @staticmethod
    def get_maintenance_summary(city=None):
        db = get_session()

        query = (
            db.query(
                Apartment.apartment_id,
                Location.city,
                func.sum(MaintenanceRequest.cost).label("total_cost"),
                func.count(MaintenanceRequest.maintenance_request_id).label("count")
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
            rows.append({
                "apartment_id": apt_id,
                "city": city_name,
                "total_cost": total_cost or 0,
                "count": count
            })

        return rows