from typing import List, Dict, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from database.models import MaintenanceRequest, Tenant, Apartment, Lease


class MaintenanceService:
    def __init__(self, db: Session):
        self.db = db

    # create request (tenant or staff)
    def create_request(
        self,
        tenant_id: int,
        apartment_id: int,
        description: str,
        priority: str = "Medium",
    ) -> bool:
        try:
            # validate tenant
            tenant = (
                self.db.query(Tenant)
                .filter(Tenant.tenant_id == tenant_id, Tenant.is_active == True)
                .first()
            )
            if not tenant:
                return False

            # validate apartment
            apt = (
                self.db.query(Apartment)
                .filter(Apartment.apartment_id == apartment_id, Apartment.is_active == True)
                .first()
            )
            if not apt:
                return False

            # find active lease
            lease = (
                self.db.query(Lease)
                .filter(
                    Lease.tenant_id == tenant_id,
                    Lease.apartment_id == apartment_id,
                    Lease.is_active == True,
                )
                .first()
            )
            if not lease:
                return False

            req = MaintenanceRequest(
                tenant_id=tenant_id,
                apartment_id=apartment_id,
                lease_id=lease.lease_id,
                description=description,
                priority=priority,
                status="Pending",
                submitted_at=datetime.now(),
                scheduled_date=None,
                resolved_at=None,
                time_taken_hours=None,
                cost=None,
                notes=None,
            )
            self.db.add(req)
            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Create Maintenance Error: {e}")
            return False

    # staff view
    def get_all_requests(self) -> List[Dict]:
        try:
            rows = (
                self.db.query(MaintenanceRequest, Tenant, Apartment)
                .join(Tenant, MaintenanceRequest.tenant_id == Tenant.tenant_id)
                .join(Apartment, MaintenanceRequest.apartment_id == Apartment.apartment_id)
                .all()
            )

            data: List[Dict] = []
            for req, tenant, apt in rows:
                loc = apt.location
                city = loc.city if loc else ""
                apt_label = f"{city} - Apt {apt.apartment_id}"

                data.append(
                    {
                        "request_id": req.maintenance_request_id,
                        "tenant_name": f"{tenant.first_name} {tenant.last_name}",
                        "apartment_label": apt_label,
                        "description": req.description,
                        "priority": req.priority,
                        "status": req.status,
                        "submitted_at": req.submitted_at.strftime("%Y-%m-%d %H:%M")
                        if req.submitted_at else "",
                        "resolved_at": req.resolved_at.strftime("%Y-%m-%d %H:%M")
                        if req.resolved_at else None,
                        "time_taken_hours": req.time_taken_hours,
                        "cost": req.cost,
                        "notes": req.notes,
                    }
                )
            return data

        except Exception as e:
            print(f"Fetch Maintenance Error: {e}")
            return []

    # tenant view
    def get_requests_for_tenant(self, tenant_id: int) -> List[Dict]:
        try:
            rows = (
                self.db.query(MaintenanceRequest)
                .filter(MaintenanceRequest.tenant_id == tenant_id)
                .order_by(MaintenanceRequest.submitted_at.desc())
                .all()
            )

            data: List[Dict] = []
            for req in rows:
                data.append(
                    {
                        "request_id": req.maintenance_request_id,
                        "description": req.description,
                        "priority": req.priority,
                        "status": req.status,
                        "submitted_at": req.submitted_at.strftime("%Y-%m-%d %H:%M")
                        if req.submitted_at else "",
                        "resolved_at": req.resolved_at.strftime("%Y-%m-%d %H:%M")
                        if req.resolved_at else None,
                    }
                )
            return data

        except Exception as e:
            print(f"Fetch Tenant Maintenance Error: {e}")
            return []

    # staff update
    def update_request(
        self,
        request_id: int,
        status: str,
        time_taken_hours: Optional[float] = None,
        cost: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> bool:
        try:
            req = (
                self.db.query(MaintenanceRequest)
                .filter(MaintenanceRequest.maintenance_request_id == request_id)
                .first()
            )
            if not req:
                return False

            req.status = status or req.status
            req.time_taken_hours = time_taken_hours if time_taken_hours is not None else req.time_taken_hours
            req.cost = cost if cost is not None else req.cost
            req.notes = notes or req.notes

            if status == "Completed" and req.resolved_at is None:
                req.resolved_at = datetime.now()

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Update Maintenance Error: {e}")
            return False

    # delete (hard delete)
    def delete_request(self, request_id: int) -> bool:
        try:
            req = (
                self.db.query(MaintenanceRequest)
                .filter(MaintenanceRequest.maintenance_request_id == request_id)
                .first()
            )
            if not req:
                return False

            self.db.delete(req)
            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Delete Maintenance Error: {e}")
            return False