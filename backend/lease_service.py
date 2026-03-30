from typing import List, Dict, Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from database.models import Lease, Tenant, Apartment


class LeaseService:
    def __init__(self, db: Session):
        # store db session
        self.db = db

    # create lease and mark apartment occupied
    def create_lease(
        self,
        tenant_id: str,
        apartment_id: str,
        start_date: str,
        duration_months: str,
        rent: str,
        deposit: str,
    ) -> bool:
        try:
            t_id = int(tenant_id)
            a_id = int(apartment_id)
            months = int(duration_months or 12)
            monthly_rent = int(float(rent))
            deposit_amount = int(float(deposit))

            # basic existence check
            tenant = (
                self.db.query(Tenant)
                .filter(Tenant.tenant_id == t_id, Tenant.is_active == True)
                .first()
            )
            apt = (
                self.db.query(Apartment)
                .filter(
                    Apartment.apartment_id == a_id,
                    Apartment.is_active == True,
                )
                .first()
            )
            if not tenant or not apt:
                return False

            # simple month approximation (30 days * months)
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            end_dt = start_dt + timedelta(days=months * 30)

            lease = Lease(
                tenant_id=t_id,
                apartment_id=a_id,
                start_date=start_dt,
                end_date=end_dt,
                monthly_rent=monthly_rent,
                deposit_amount=deposit_amount,
                is_active=True,
            )
            self.db.add(lease)

            # occupancy flip
            apt.is_available = False

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Create Lease Error: {e}")
            return False

    # list active leases with tenant names
    def get_all_leases(self) -> List[Dict]:
        try:
            leases = (
                self.db.query(Lease, Tenant)
                .join(Tenant, Lease.tenant_id == Tenant.tenant_id)
                .filter(Lease.is_active == True, Tenant.is_active == True)
                .all()
            )

            data: List[Dict] = []
            for lease, tenant in leases:
                data.append(
                    {
                        "lease_id": lease.lease_id,
                        "tenant_id": lease.tenant_id,
                        "apartment_id": lease.apartment_id,
                        "start_date": lease.start_date.strftime("%Y-%m-%d"),
                        "end_date": lease.end_date.strftime("%Y-%m-%d"),
                        "monthly_rent": lease.monthly_rent,
                        "deposit_amount": lease.deposit_amount,
                        "is_active": 1 if lease.is_active else 0,
                        "first_name": tenant.first_name,
                        "last_name": tenant.last_name,
                    }
                )
            return data
        except Exception as e:
            print(f"Fetch Leases Error: {e}")
            return []

    # early termination with 5% penalty and availability flip
    def terminate_lease(self, lease_id: int, apartment_id: int) -> Optional[float]:
        try:
            lease = (
                self.db.query(Lease)
                .filter(Lease.lease_id == lease_id)
                .first()
            )
            if not lease:
                return None

            apt = (
                self.db.query(Apartment)
                .filter(Apartment.apartment_id == apartment_id)
                .first()
            )
            if not apt:
                return None

            # penalty = 5% of monthly rent
            penalty = float(lease.monthly_rent) * 0.05

            # mark lease inactive
            lease.is_active = False

            # free apartment
            apt.is_available = True

            self.db.commit()
            return penalty
        except Exception as e:
            self.db.rollback()
            print(f"Termination Error: {e}")
            return None