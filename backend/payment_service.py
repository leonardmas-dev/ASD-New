from datetime import datetime
from typing import List, Dict, Optional

from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import Payment, Lease, Tenant, Apartment


class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    # create a payment record for a lease
    def create_payment(
        self,
        lease_id: int,
        amount_due: int,
        due_date: datetime,
    ) -> bool:
        try:
            pay = Payment(
                lease_id=lease_id,
                amount_due=amount_due,
                amount_paid=0,
                due_date=due_date,
                payment_date=None,
                is_late=False,
                late_fee=0,
                status="Unpaid",
            )
            self.db.add(pay)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Create Payment Error: {e}")
            return False

    # mark payment as paid
    def record_payment(
        self,
        payment_id: int,
        amount_paid: int,
    ) -> bool:
        try:
            pay = (
                self.db.query(Payment)
                .filter(Payment.payment_id == payment_id)
                .first()
            )
            if not pay:
                return False

            pay.amount_paid = amount_paid
            pay.payment_date = datetime.now()

            # late logic
            if pay.payment_date > pay.due_date:
                pay.is_late = True
                pay.late_fee = 25  # fixed fee of 25 pounds
                pay.status = "Late Paid"
            else:
                pay.is_late = False
                pay.late_fee = 0
                pay.status = "Paid"

            self.db.commit()
            return True

        except Exception as e:
            self.db.rollback()
            print(f"Record Payment Error: {e}")
            return False

    # staff view: all payments
    def get_all_payments(self) -> List[Dict]:
        try:
            rows = (
                self.db.query(Payment, Lease, Tenant, Apartment)
                .join(Lease, Payment.lease_id == Lease.lease_id)
                .join(Tenant, Lease.tenant_id == Tenant.tenant_id)
                .join(Apartment, Lease.apartment_id == Apartment.apartment_id)
                .all()
            )

            data = []
            for pay, lease, tenant, apt in rows:
                loc = apt.location
                city = loc.city if loc else ""

                data.append(
                    {
                        "payment_id": pay.payment_id,
                        "tenant_name": f"{tenant.first_name} {tenant.last_name}",
                        "apartment_label": f"{city} - Apt {apt.apartment_id}",
                        "amount_due": pay.amount_due,
                        "amount_paid": pay.amount_paid,
                        "due_date": pay.due_date.strftime("%Y-%m-%d"),
                        "payment_date": pay.payment_date.strftime("%Y-%m-%d")
                        if pay.payment_date else None,
                        "status": pay.status,
                        "late_fee": pay.late_fee,
                        "is_late": pay.is_late,
                    }
                )
            return data

        except Exception as e:
            print(f"Fetch Payments Error: {e}")
            return []

    # tenant view: payments for their lease(s)
    def get_payments_for_tenant(self, tenant_id: int) -> List[Dict]:
        try:
            rows = (
                self.db.query(Payment, Lease)
                .join(Lease, Payment.lease_id == Lease.lease_id)
                .filter(Lease.tenant_id == tenant_id)
                .order_by(Payment.due_date.desc())
                .all()
            )

            data = []
            for pay, lease in rows:
                data.append(
                    {
                        "payment_id": pay.payment_id,
                        "amount_due": pay.amount_due,
                        "amount_paid": pay.amount_paid,
                        "due_date": pay.due_date.strftime("%Y-%m-%d"),
                        "payment_date": pay.payment_date.strftime("%Y-%m-%d")
                        if pay.payment_date else None,
                        "status": pay.status,
                        "late_fee": pay.late_fee,
                        "is_late": pay.is_late,
                    }
                )
            return data

        except Exception as e:
            print(f"Fetch Tenant Payments Error: {e}")
            return []

    # tenant graph: monthly totals
    def get_monthly_payment_summary(self, tenant_id: int) -> List[Dict]:
        try:
            rows = (
                self.db.query(
                    func.strftime("%Y-%m", Payment.due_date).label("month"),
                    func.sum(Payment.amount_paid).label("paid"),
                    func.sum(Payment.amount_due).label("due"),
                )
                .join(Lease, Payment.lease_id == Lease.lease_id)
                .filter(Lease.tenant_id == tenant_id)
                .group_by("month")
                .order_by("month")
                .all()
            )

            data = []
            for month, paid, due in rows:
                data.append(
                    {
                        "month": month,
                        "paid": paid or 0,
                        "due": due or 0,
                    }
                )
            return data

        except Exception as e:
            print(f"Monthly Summary Error: {e}")
            return []

    # tenant graph: neighbour comparison
    def get_neighbour_comparison(self, tenant_id: int) -> Dict:
        try:
            # tenant total
            tenant_total = (
                self.db.query(func.sum(Payment.amount_paid))
                .join(Lease, Payment.lease_id == Lease.lease_id)
                .filter(Lease.tenant_id == tenant_id)
                .scalar()
            ) or 0

            # find tenant's location
            lease = (
                self.db.query(Lease)
                .filter(Lease.tenant_id == tenant_id, Lease.is_active == True)
                .first()
            )
            if not lease:
                return {"tenant_total": 0, "neighbours_avg": 0}

            apt = lease.apartment
            loc = apt.location

            # neighbours = all tenants in same location
            neighbours_avg = (
                self.db.query(func.avg(Payment.amount_paid))
                .join(Lease, Payment.lease_id == Lease.lease_id)
                .join(Apartment, Lease.apartment_id == Apartment.apartment_id)
                .filter(Apartment.location_id == loc.location_id)
                .scalar()
            ) or 0

            return {
                "tenant_total": tenant_total,
                "neighbours_avg": round(neighbours_avg, 2),
            }

        except Exception as e:
            print(f"Neighbour Comparison Error: {e}")
            return {"tenant_total": 0, "neighbours_avg": 0}