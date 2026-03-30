from typing import List, Dict, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from database.models import MaintenanceRequest, Tenant, Apartment, Lease


class MaintenanceService:
    def __init__(self, db: Session):
        # store db session
        self.db = db

    # create request (tenant or staff on behalf of tenant)
    def create_request(
        self,
        tenant_id: int,
        apartment_id: int,
        category: str,
        description: str,
        priority: str = "Medium",
        created_by_staff: bool = False,
    ) -> bool:
        try:
            tenant = (
                self.db.query(Tenant)
                .filter(Tenant.tenant_id == tenant_id, Tenant.is_active == True)
                .first()
            )
            apt = (
                self.db.query(Apartment)
                .filter(Apartment.apartment_id == apartment_id, Apartment.is_active == True)
                .first()
            )
            if not tenant or not apt:
                return False

            req = MaintenanceRequest(
                tenant_id=tenant_id,
                apartment_id=apartment_id,
                category=category or "General",
                description=description,
                priority=priority or "Medium",
                status="Pending",
                created_at=datetime.now(),
                created_by_staff=created_by_staff,
                resolved_at=None,
                resolution_notes=None,
                time_taken_hours=None,
                cost=None,
                is_active=True,
            )
            self.db.add(req)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Create Maintenance Error: {e}")
            return False

    # list all active requests (staff view)
    def get_all_requests(self) -> List[Dict]:
        try:
            rows = (
                self.db.query(MaintenanceRequest, Tenant, Apartment)
                .join(Tenant, MaintenanceRequest.tenant_id == Tenant.tenant_id)
                .join(Apartment, MaintenanceRequest.apartment_id == Apartment.apartment_id)
                .filter(MaintenanceRequest.is_active == True)
                .all()
            )

            data: List[Dict] = []
            for req, tenant, apt in rows:
                data.append(
                    {
                        "request_id": req.request_id,
                        "tenant_id": req.tenant_id,
                        "tenant_name": f"{tenant.first_name} {tenant.last_name}",
                        "apartment_id": req.apartment_id,
                        "apartment_label": f"{apt.city} - {apt.apartment_number}"
                        if hasattr(apt, "city") and hasattr(apt, "apartment_number")
                        else str(req.apartment_id),
                        "category": req.category,
                        "description": req.description,
                        "priority": req.priority,
                        "status": req.status,
                        "created_at": req.created_at.strftime("%Y-%m-%d %H:%M")
                        if req.created_at
                        else "",
                        "resolved_at": req.resolved_at.strftime("%Y-%m-%d %H:%M")
                        if req.resolved_at
                        else None,
                        "time_taken_hours": req.time_taken_hours,
                        "cost": req.cost,
                    }
                )
            return data
        except Exception as e:
            print(f"Fetch Maintenance Error: {e}")
            return []

    # list requests for a specific tenant (tenant portal)
    def get_requests_for_tenant(self, tenant_id: int) -> List[Dict]:
        try:
            rows = (
                self.db.query(MaintenanceRequest)
                .filter(
                    MaintenanceRequest.tenant_id == tenant_id,
                    MaintenanceRequest.is_active == True,
                )
                .order_by(MaintenanceRequest.created_at.desc())
                .all()
            )

            data: List[Dict] = []
            for req in rows:
                data.append(
                    {
                        "request_id": req.request_id,
                        "apartment_id": req.apartment_id,
                        "category": req.category,
                        "description": req.description,
                        "priority": req.priority,
                        "status": req.status,
                        "created_at": req.created_at.strftime("%Y-%m-%d %H:%M")
                        if req.created_at
                        else "",
                        "resolved_at": req.resolved_at.strftime("%Y-%m-%d %H:%M")
                        if req.resolved_at
                        else None,
                    }
                )
            return data
        except Exception as e:
            print(f"Fetch Tenant Maintenance Error: {e}")
            return []

    # update status and resolution details (staff)
    def update_request(
        self,
        request_id: int,
        status: str,
        resolution_notes: Optional[str] = None,
        time_taken_hours: Optional[float] = None,
        cost: Optional[float] = None,
    ) -> bool:
        try:
            req = (
                self.db.query(MaintenanceRequest)
                .filter(MaintenanceRequest.request_id == request_id, MaintenanceRequest.is_active == True)
                .first()
            )
            if not req:
                return False

            req.status = status or req.status
            req.resolution_notes = resolution_notes or req.resolution_notes
            req.time_taken_hours = (
                time_taken_hours if time_taken_hours is not None else req.time_taken_hours
            )
            req.cost = cost if cost is not None else req.cost

            if status == "Completed" and req.resolved_at is None:
                req.resolved_at = datetime.now()

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Update Maintenance Error: {e}")
            return False

    # soft delete request
    def delete_request(self, request_id: int) -> bool:
        try:
            req = (
                self.db.query(MaintenanceRequest)
                .filter(MaintenanceRequest.request_id == request_id)
                .first()
            )
            if not req:
                return False

            req.is_active = False
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Delete Maintenance Error: {e}")
            return False