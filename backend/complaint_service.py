# Student: Ishak Askar     StudentID: 24023614

from typing import List, Dict, Optional
from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from database.models import Complaint, Tenant, Lease, Apartment


class ComplaintService:
    def __init__(self, db: Session):
        self.db = db

    def create_complaint(self, tenant_id: int, apartment_id: int, description: str) -> bool:
        """Create a complaint for a tenant with an active lease."""
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

            comp = Complaint(
                tenant_id=tenant_id,
                lease_id=lease.lease_id,
                description=description,
                submitted_at=datetime.now(),
                status="Pending",
                resolved_at=None,
                resolution_notes=None,
            )

            self.db.add(comp)
            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Create Complaint Error: {e}")
            return False

    def get_all_complaints(self) -> List[Dict]:
        """Return all complaints with tenant + apartment info."""
        try:
            rows = (
                self.db.query(Complaint)
                .options(
                    joinedload(Complaint.tenant),
                    joinedload(Complaint.lease).joinedload(Lease.apartment).joinedload(Apartment.location),
                )
                .all()
            )

            data = []
            for comp in rows:
                tenant = comp.tenant
                apt = comp.lease.apartment
                loc = apt.location

                apartment_label = f"{loc.city} - Apt {apt.apartment_id}"

                data.append(
                    {
                        "complaint_id": comp.complaint_id,
                        "tenant_id": comp.tenant_id,
                        "tenant_name": f"{tenant.first_name} {tenant.last_name}",
                        "apartment_id": apt.apartment_id,
                        "apartment_label": apartment_label,
                        "description": comp.description,
                        "status": comp.status,
                        "submitted_at": comp.submitted_at.strftime("%Y-%m-%d %H:%M")
                        if comp.submitted_at else "",
                        "resolved_at": comp.resolved_at.strftime("%Y-%m-%d %H:%M")
                        if comp.resolved_at else None,
                        "notes": comp.resolution_notes,
                    }
                )

            return data

        except Exception as e:
            print(f"Fetch Complaints Error: {e}")
            return []

    def get_complaints_for_tenant(self, tenant_id: int) -> List[Dict]:
        """Return complaints for tenant portal."""
        try:
            rows = (
                self.db.query(Complaint)
                .filter(Complaint.tenant_id == tenant_id)
                .order_by(Complaint.submitted_at.desc())
                .all()
            )

            data = []
            for comp in rows:
                data.append(
                    {
                        "complaint_id": comp.complaint_id,
                        "description": comp.description,
                        "status": comp.status,
                        "submitted_at": comp.submitted_at.strftime("%Y-%m-%d %H:%M")
                        if comp.submitted_at else "",
                        "resolved_at": comp.resolved_at.strftime("%Y-%m-%d %H:%M")
                        if comp.resolved_at else None,
                        "staff_response": comp.resolution_notes,
                    }
                )

            return data

        except Exception as e:
            print(f"Fetch Tenant Complaints Error: {e}")
            return []

    def get_complaint_by_id(self, complaint_id: int) -> Optional[Dict]:
        """Return a single complaint with details."""
        try:
            comp = (
                self.db.query(Complaint)
                .filter(Complaint.complaint_id == complaint_id)
                .first()
            )
            if not comp:
                return None

            return {
                "complaint_id": comp.complaint_id,
                "tenant_id": comp.tenant_id,
                "description": comp.description,
                "status": comp.status,
                "submitted_at": comp.submitted_at.strftime("%Y-%m-%d %H:%M")
                if comp.submitted_at else "",
                "resolved_at": comp.resolved_at.strftime("%Y-%m-%d %H:%M")
                if comp.resolved_at else None,
                "notes": comp.resolution_notes,
            }

        except Exception as e:
            print(f"Fetch Complaint Error: {e}")
            return None

    def update_complaint(self, complaint_id: int, status: str, notes: Optional[str]) -> bool:
        """Update complaint status and notes."""
        try:
            comp = (
                self.db.query(Complaint)
                .filter(Complaint.complaint_id == complaint_id)
                .first()
            )
            if not comp:
                return False

            comp.status = status or comp.status
            comp.resolution_notes = notes or comp.resolution_notes

            if status == "Resolved" and comp.resolved_at is None:
                comp.resolved_at = datetime.now()

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Update Complaint Error: {e}")
            return False

    def delete_complaint(self, complaint_id: int) -> bool:
        """Hard delete a complaint."""
        try:
            comp = (
                self.db.query(Complaint)
                .filter(Complaint.complaint_id == complaint_id)
                .first()
            )
            if not comp:
                return False

            self.db.delete(comp)
            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Delete Complaint Error: {e}")
            return False