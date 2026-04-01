# Student: Yaseen Sassi     StudentID: 24023127

from datetime import datetime
from typing import List, Dict

from sqlalchemy.orm import Session
from sqlalchemy import func

from database.models import Payment, Lease, Tenant, Apartment


class PaymentService:
    def __init__(self, db: Session):
        self.db = db

    # create a payment record for an active lease only
    def create_payment(self, lease_id: int, amount_due: int, due_date: datetime) -> bool:
        try:
            lease = self.db.query(Lease).filter(Lease.lease_id == lease_id).first()
            if not lease or not lease.is_active:
                return False

            existing = (
                self.db.query(Payment)
                .filter(Payment.lease_id == lease_id, Payment.due_date == due_date)
                .first()
            )
            if existing:
                return False

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
    def record_payment(self, payment_id: int, amount_paid: int) -> bool:
        try:
            pay = (
                self.db.query(Payment)
                .filter(Payment.payment_id == payment_id)
                .first()
            )
            if not pay:
                return False

            if not pay.lease.is_active:
                return False

            pay.amount_paid = amount_paid
            pay.payment_date = datetime.now()

            if pay.payment_date > pay.due_date:
                pay.is_late = True
                pay.late_fee = 25
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

    # view all payments
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

    # current payments table
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

    # payment history (used by tenant_portal/payment_history.py)
    class _PaymentHistoryRow:
        def __init__(self, p: Payment):
            self.payment_id = p.payment_id
            self.amount_due = p.amount_due
            self.amount_paid = p.amount_paid
            self.due_date = p.due_date
            self.paid_at = p.payment_date
            self.status = p.status
            self.late_fee = p.late_fee
            self.is_late = p.is_late

    def get_payment_history_for_tenant(self, tenant_id: int):
        try:
            rows = (
                self.db.query(Payment)
                .join(Lease, Payment.lease_id == Lease.lease_id)
                .filter(Lease.tenant_id == tenant_id)
                .order_by(Payment.due_date.desc())
                .all()
            )
            return [self._PaymentHistoryRow(p) for p in rows]

        except Exception as e:
            print(f"Tenant Payment History Error: {e}")
            return []

    # payment sequence for graphing (Payment 1, Payment 2, Payment 3 etc.)
    def get_payment_sequence_for_tenant(self, tenant_id: int):
        try:
            rows = (
                self.db.query(Payment)
                .join(Lease, Payment.lease_id == Lease.lease_id)
                .filter(Lease.tenant_id == tenant_id)
                .order_by(Payment.payment_id.asc())
                .all()
            )

            data = []
            for idx, p in enumerate(rows, start=1):
                data.append({
                    "index": idx,
                    "paid": float(p.amount_paid or 0),
                    "due": float(p.amount_due or 0),
                    "status": p.status
                })

            return data

        except Exception as e:
            print(f"Payment Sequence Error: {e}")
            return []

    #neighbour comparison
    def get_neighbour_comparison(self, tenant_id: int) -> Dict:
        try:
            tenant_total = (
                self.db.query(func.sum(Payment.amount_paid))
                .join(Lease, Payment.lease_id == Lease.lease_id)
                .filter(Lease.tenant_id == tenant_id)
                .scalar()
            ) or 0

            lease = (
                self.db.query(Lease)
                .filter(Lease.tenant_id == tenant_id, Lease.is_active == True)
                .first()
            )
            if not lease:
                return {"tenant_total": 0, "neighbours_avg": 0}

            apt = lease.apartment
            loc = apt.location

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