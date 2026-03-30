from typing import List, Dict, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from database.models import Complaint, Tenant, Apartment


class ComplaintService:
    def __init__(self, db: Session):
        # store db session
        self.db = db

    # create complaint (tenant or staff on behalf of tenant)
    def create_complaint(
        self,
        tenant_id: int,
        apartment_id: int,
        category: str,
        description: str,
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

            comp = Complaint(
                tenant_id=tenant_id,
                apartment_id=apartment_id,
                category=category or "General",
                description=description,
                status="Open",
                created_at=datetime.now(),
                created_by_staff=created_by_staff,
                resolved_at=None,
                resolution_notes=None,
                is_active=True,
            )
            self.db.add(comp)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Create Complaint Error: {e}")
            return False

    # list all active complaints (staff view)
    def get_all_complaints(self) -> List[Dict]:
        try:
            rows = (
                self.db.query(Complaint, Tenant, Apartment)
                .join(Tenant, Complaint.tenant_id == Tenant.tenant_id)
                .join(Apartment, Complaint.apartment_id == Apartment.apartment_id)
                .filter(Complaint.is_active == True)
                .all()
            )

            data: List[Dict] = []
            for comp, tenant, apt in rows:
                data.append(
                    {
                        "complaint_id": comp.complaint_id,
                        "tenant_id": comp.tenant_id,
                        "tenant_name": f"{tenant.first_name} {tenant.last_name}",
                        "apartment_id": comp.apartment_id,
                        "category": comp.category,
                        "description": comp.description,
                        "status": comp.status,
                        "created_at": comp.created_at.strftime("%Y-%m-%d %H:%M"),
                        "resolved_at": comp.resolved_at.strftime("%Y-%m-%d %H:%M") if comp.resolved_at else None,
                    }
                )
            return data
        except Exception as e:
            print(f"Fetch Complaints Error: {e}")
            return []

    # list complaints for a specific tenant (tenant portal)
    def get_complaints_for_tenant(self, tenant_id: int) -> List[Dict]:
        try:
            rows = (
                self.db.query(Complaint)
                .filter(
                    Complaint.tenant_id == tenant_id,
                    Complaint.is_active == True,
                )
                .order_by(Complaint.created_at.desc())
                .all()
            )

            data: List[Dict] = []
            for comp in rows:
                data.append(
                    {
                        "complaint_id": comp.complaint_id,
                        "apartment_id": comp.apartment_id,
                        "category": comp.category,
                        "description": comp.description,
                        "status": comp.status,
                        "created_at": comp.created_at.strftime("%Y-%m-%d %H:%M"),
                        "resolved_at": comp.resolved_at.strftime("%Y-%m-%d %H:%M") if comp.resolved_at else None,
                    }
                )
            return data
        except Exception as e:
            print(f"Fetch Tenant Complaints Error: {e}")
            return []

    # update status and resolution details (staff)
    def update_complaint(
        self,
        complaint_id: int,
        status: str,
        resolution_notes: Optional[str] = None,
    ) -> bool:
        try:
            comp = (
                self.db.query(Complaint)
                .filter(Complaint.complaint_id == complaint_id, Complaint.is_active == True)
                .first()
            )
            if not comp:
                return False

            comp.status = status or comp.status
            comp.resolution_notes = resolution_notes or comp.resolution_notes

            # set resolved timestamp when marked resolved
            if status == "Resolved" and comp.resolved_at is None:
                comp.resolved_at = datetime.now()

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Update Complaint Error: {e}")
            return False

    # soft delete complaint
    def delete_complaint(self, complaint_id: int) -> bool:
        try:
            comp = (
                self.db.query(Complaint)
                .filter(Complaint.complaint_id == complaint_id)
                .first()
            )
            if not comp:
                return False

            comp.is_active = False
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Delete Complaint Error: {e}")
            return False