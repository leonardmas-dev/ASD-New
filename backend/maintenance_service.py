# Student: Ishak Askar    StudentID: 24023614

from typing import List, Dict, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from database.models import (
    MaintenanceRequest,
    MaintenanceStaffAssignment,
    Tenant,
    Apartment,
    Lease,
    User,
)

class MaintenanceService:
    def __init__(self, db: Session):
        self.db = db
    def create_request(
        self,
        tenant_id: int,
        apartment_id: int,
        description: str,
        priority: str,
        staff_user_id: int,
        status: str = "Pending",
        scheduled_date: Optional[datetime] = None,
        time_taken_hours: Optional[float] = None,
        cost: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> bool:
        try:
            tenant = (
                self.db.query(Tenant)
                .filter(Tenant.tenant_id == tenant_id, Tenant.is_active == True)
                .first()
            )
            if not tenant:
                return False

            apt = (
                self.db.query(Apartment)
                .filter(Apartment.apartment_id == apartment_id, Apartment.is_active == True)
                .first()
            )
            if not apt:
                return False

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

            now = datetime.now()

            req = MaintenanceRequest(
                tenant_id=tenant_id,
                apartment_id=apartment_id,
                lease_id=lease.lease_id,
                description=description,
                priority=priority,
                status=status,
                submitted_at=now,
                scheduled_date=scheduled_date,
                resolved_at=None,
                time_taken_hours=time_taken_hours,
                cost=cost,
                notes=notes,
            )
            self.db.add(req)
            self.db.commit()

            if staff_user_id is not None:
                assignment = MaintenanceStaffAssignment(
                    maintenance_request_id=req.maintenance_request_id,
                    user_id=staff_user_id,
                    assigned_at=now,
                    notes=None,
                )
                self.db.add(assignment)
                self.db.commit()

            return True

        except Exception as e:
            self.db.rollback()
            print(f"Create Maintenance Error: {e}")
            return False
    def get_maintenance_staff(self) -> List[Dict]:
        try:
            rows = (
                self.db.query(User)
                .filter(User.role == "MaintenanceStaff", User.is_active == True)
                .all()
            )

            return [
                {
                    "user_id": u.user_id,
                    "name": f"{u.first_name} {u.last_name} - Maintenance Staff",
                }
                for u in rows
            ]

        except Exception as e:
            print(f"Fetch Staff Error: {e}")
            return []

    def get_assigned_staff(self, request_id: int) -> Optional[Dict]:
        try:
            assignment = (
                self.db.query(MaintenanceStaffAssignment)
                .options(joinedload(MaintenanceStaffAssignment.user))
                .filter(MaintenanceStaffAssignment.maintenance_request_id == request_id)
                .order_by(MaintenanceStaffAssignment.assigned_at.desc())
                .first()
            )

            if not assignment:
                return None

            user = assignment.user
            return {
                "user_id": user.user_id,
                "name": f"{user.first_name} {user.last_name} - Maintenance Staff",
            }

        except Exception as e:
            print(f"Fetch Assigned Staff Error: {e}")
            return None

    #  Update request
    def update_request(
        self,
        request_id: int,
        status: Optional[str],
        time_taken_hours: Optional[float],
        cost: Optional[float],
        notes: Optional[str],
        staff_user_id: Optional[int],
        scheduled_date: Optional[datetime] = None,
    ) -> bool:
        try:
            req = (
                self.db.query(MaintenanceRequest)
                .filter(MaintenanceRequest.maintenance_request_id == request_id)
                .first()
            )
            if not req:
                return False

            if status:
                req.status = status

            if scheduled_date is not None:
                req.scheduled_date = scheduled_date

            if time_taken_hours is not None:
                req.time_taken_hours = time_taken_hours

            if cost is not None:
                req.cost = cost

            if notes:
                req.notes = notes

            if status == "Completed" and req.resolved_at is None:
                req.resolved_at = datetime.now()
                if req.submitted_at and req.time_taken_hours is None:
                    delta = req.resolved_at - req.submitted_at
                    req.time_taken_hours = round(delta.total_seconds() / 3600, 2)

            self.db.commit()

            if staff_user_id:
                assignment = MaintenanceStaffAssignment(
                    maintenance_request_id=request_id,
                    user_id=staff_user_id,
                    assigned_at=datetime.now(),
                    notes=None,
                )
                self.db.add(assignment)
                self.db.commit()

            return True

        except Exception as e:
            self.db.rollback()
            print(f"Update Maintenance Error: {e}")
            return False
    def get_all_requests(self) -> List[Dict]:
        try:
            rows = (
                self.db.query(MaintenanceRequest)
                .options(
                    joinedload(MaintenanceRequest.tenant),
                    joinedload(MaintenanceRequest.apartment).joinedload(Apartment.location),
                )
                .all()
            )

            data: List[Dict] = []
            for req in rows:
                tenant = req.tenant
                apt = req.apartment
                loc = apt.location

                staff = self.get_assigned_staff(req.maintenance_request_id)
                staff_name = staff["name"] if staff else "Unassigned"

                data.append(
                    {
                        "request_id": req.maintenance_request_id,
                        "tenant_name": f"{tenant.first_name} {tenant.last_name}",
                        "apartment_label": f"{loc.city} - Apt {apt.apartment_id}",
                        "description": req.description,
                        "priority": req.priority,
                        "status": req.status,
                        "submitted_at": req.submitted_at,
                        "scheduled_date": req.scheduled_date,
                        "resolved_at": req.resolved_at,
                        "time_taken_hours": req.time_taken_hours,
                        "cost": req.cost,
                        "notes": req.notes,
                        "assigned_staff": staff_name,
                    }
                )

            return data

        except Exception as e:
            print(f"Fetch Maintenance Error: {e}")
            return []
    def get_requests_for_tenant(self, tenant_id: int) -> List[Dict]:
        """
        Returns all maintenance requests submitted by a tenant.
        Used by tenant portal.
        """
        try:
            rows = (
                self.db.query(MaintenanceRequest)
                .options(
                    joinedload(MaintenanceRequest.apartment).joinedload(Apartment.location)
                )
                .filter(MaintenanceRequest.tenant_id == tenant_id)
                .order_by(MaintenanceRequest.submitted_at.desc())
                .all()
            )

            data = []
            for req in rows:
                apt = req.apartment
                loc = apt.location
                staff = self.get_assigned_staff(req.maintenance_request_id)
                staff_name = staff["name"] if staff else "Unassigned"

                data.append(
                    {
                        "request_id": req.maintenance_request_id,
                        "description": req.description,
                        "priority": req.priority,
                        "status": req.status,
                        "submitted_at": req.submitted_at,
                        "scheduled_date": req.scheduled_date,
                        "resolved_at": req.resolved_at,
                        "time_taken_hours": req.time_taken_hours,
                        "cost": req.cost,
                        "notes": req.notes,
                        "apartment_label": f"{loc.city} - Apt {apt.apartment_id}",
                        "assigned_staff": staff_name,
                    }
                )

            return data

        except Exception as e:
            print(f"Tenant Maintenance Error: {e}")
            return []