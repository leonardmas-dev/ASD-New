from typing import List, Dict, Optional
from datetime import datetime

from sqlalchemy.orm import Session

from database.models import Complaint, Tenant, Lease, Apartment


class ComplaintService:
    def __init__(self, db: Session):
        # store db session
        self.db = db

    # create complaint (tenant or staff on behalf of tenant)
    def create_complaint(
        self,
        tenant_id: int,
        apartment_id: int,
        description: str,
    ) -> bool:
        try:
            # validate active tenant
            tenant = (
                self.db.query(Tenant)
                .filter(Tenant.tenant_id == tenant_id, Tenant.is_active == True)
                .first()
            )
            if not tenant:
                return False

            # validate active apartment
            apt = (
                self.db.query(Apartment)
                .filter(Apartment.apartment_id == apartment_id, Apartment.is_active == True)
                .first()
            )
            if not apt:
                return False

            # find an active lease for this tenant + apartment
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
                # no active lease means no complaint
                return False

            comp = Complaint(
                tenant_id=tenant_id,
                lease_id=lease.lease_id,
                description=description,
                submitted_at=datetime.now(),
                status="Open",
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

    # list all complaints (staff view)
    def get_all_complaints(self) -> List[Dict]:
        try:
            rows = (
                self.db.query(Complaint, Tenant, Lease, Apartment)
                .join(Tenant, Complaint.tenant_id == Tenant.tenant_id)
                .join(Lease, Complaint.lease_id == Lease.lease_id)
                .join(Apartment, Lease.apartment_id == Apartment.apartment_id)
                .all()
            )

            data: List[Dict] = []
            for comp, tenant, lease, apt in rows:
                loc = apt.location
                city = loc.city if loc else ""
                apartment_label = f"{city} - Apt {apt.apartment_id}"

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
                        if comp.submitted_at
                        else "",
                        "resolved_at": comp.resolved_at.strftime("%Y-%m-%d %H:%M")
                        if comp.resolved_at
                        else None,
                        "resolution_notes": comp.resolution_notes,
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
                .filter(Complaint.tenant_id == tenant_id)
                .order_by(Complaint.submitted_at.desc())
                .all()
            )

            data: List[Dict] = []
            for comp in rows:
                data.append(
                    {
                        "complaint_id": comp.complaint_id,
                        "description": comp.description,
                        "status": comp.status,
                        "submitted_at": comp.submitted_at.strftime("%Y-%m-%d %H:%M")
                        if comp.submitted_at
                        else "",
                        "resolved_at": comp.resolved_at.strftime("%Y-%m-%d %H:%M")
                        if comp.resolved_at
                        else None,
                        "resolution_notes": comp.resolution_notes,
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
                .filter(Complaint.complaint_id == complaint_id)
                .first()
            )
            if not comp:
                return False

            comp.status = status or comp.status
            comp.resolution_notes = resolution_notes or comp.resolution_notes

            if status == "Resolved" and comp.resolved_at is None:
                comp.resolved_at = datetime.now()

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Update Complaint Error: {e}")
            return False

    # delete complaint
    def delete_complaint(self, complaint_id: int) -> bool:
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