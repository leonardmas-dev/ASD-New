from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from database.session import get_session
from database.models import (
    Lease,
    Payment,
    Invoice,
    Apartment,
    Location,
    Tenant,
)

LATE_FEE_PERCENT = 0.05  # 5% late fee on amount_due


class PaymentService:
    """
    Service layer for all payment, billing, and invoice logic.
    Used by Finance Manager UI and Tenant Portal.
    """

    def __init__(self, db: Optional[Session] = None):
        self.db = db or get_session()

    # Lease / selection helpers
    def get_active_leases(self) -> List[Lease]:
        """
        Return all active leases with tenant + apartment loaded.
        Used by Finance Manager when recording payments.
        """
        return (
            self.db.query(Lease)
            .options(
                joinedload(Lease.tenant),
                joinedload(Lease.apartment).joinedload(Apartment.location),
            )
            .filter(Lease.is_active == True)
            .all()
        )

    def get_lease_by_id(self, lease_id: int) -> Optional[Lease]:
        """
        Fetch a single lease by ID with relationships.
        """
        return (
            self.db.query(Lease)
            .options(
                joinedload(Lease.tenant),
                joinedload(Lease.apartment).joinedload(Apartment.location),
            )
            .filter(Lease.lease_id == lease_id)
            .first()
        )

    # Tenant helper: get current active lease
    def get_current_active_lease_for_tenant(self, tenant_id: int) -> Optional[Lease]:
        """
        Return the current active lease for a tenant.
        Assumes at most one active lease per tenant.
        Used by tenant portal for payments.
        """
        return (
            self.db.query(Lease)
            .options(
                joinedload(Lease.apartment).joinedload(Apartment.location),
                joinedload(Lease.tenant),
            )
            .filter(
                Lease.tenant_id == tenant_id,
                Lease.is_active == True,
            )
            .first()
        )

    # Invoice logic
    def create_invoice(
        self,
        lease_id: int,
        amount_due: int,
        due_date: datetime,
        description: str = "",
    ) -> Invoice:
        """
        Create an invoice for a lease.
        Used to emulate billing without real payment processing.
        """
        invoice = Invoice(
            lease_id=lease_id,
            amount_due=amount_due,
            issue_date=datetime.utcnow(),
            due_date=due_date,
            status="Pending",
            description=description,
            is_late=False,
        )
        self.db.add(invoice)
        self.db.commit()
        self.db.refresh(invoice)
        return invoice

    def get_invoices_for_lease(self, lease_id: int) -> List[Invoice]:
        """
        Return all invoices for a given lease.
        """
        return (
            self.db.query(Invoice)
            .filter(Invoice.lease_id == lease_id)
            .order_by(Invoice.due_date.desc())
            .all()
        )

    # Payment recording + late fee logic
    def record_payment(
        self,
        lease_id: int,
        amount_due: int,
        amount_paid: int,
        due_date: datetime,
        payment_date: Optional[datetime] = None,
    ) -> Payment:
        """
        Record a payment for a lease.
        - Detect late payment
        - Apply 5% late fee if late
        - Set status accordingly
        """
        payment_date = payment_date or datetime.utcnow()

        # determine lateness
        is_late = payment_date.date() > due_date.date()
        late_fee = 0

        if is_late:
            late_fee = int(amount_due * LATE_FEE_PERCENT)

        # determine status
        if amount_paid >= amount_due + late_fee:
            status = "Paid"
        elif amount_paid > 0:
            status = "Partially Paid"
        else:
            status = "Pending"

        payment = Payment(
            lease_id=lease_id,
            amount_due=amount_due,
            amount_paid=amount_paid,
            due_date=due_date,
            payment_date=payment_date,
            is_late=is_late,
            late_fee=late_fee if is_late else None,
            status=status,
        )

        self.db.add(payment)
        self.db.commit()
        self.db.refresh(payment)
        return payment

    def mark_overdue_payments(self):
        """
        Scan all payments where due_date < today and no payment_date,
        mark them as late and update status.
        Can be called periodically or on Finance Manager actions.
        """
        today = datetime.utcnow().date()

        overdue = (
            self.db.query(Payment)
            .filter(
                Payment.payment_date.is_(None),
                Payment.due_date < datetime(today.year, today.month, today.day),
            )
            .all()
        )

        for p in overdue:
            p.is_late = True
            p.late_fee = int(p.amount_due * LATE_FEE_PERCENT)
            p.status = "Late"

        if overdue:
            self.db.commit()

    # Payment history + tenant portal support
    def get_payment_history_for_lease(self, lease_id: int) -> List[Payment]:
        """
        Return all payments for a lease, newest first.
        Used by Finance Manager and tenant portal.
        """
        return (
            self.db.query(Payment)
            .filter(Payment.lease_id == lease_id)
            .order_by(Payment.due_date.desc())
            .all()
        )

    def get_payment_history_for_tenant(self, tenant_id: int) -> List[Payment]:
        """
        Return all payments for a tenant across all leases.
        Used by tenant portal for payment history + graphs.
        """
        return (
            self.db.query(Payment)
            .join(Lease, Payment.lease_id == Lease.lease_id)
            .filter(Lease.tenant_id == tenant_id)
            .order_by(Payment.due_date.desc())
            .all()
        )

    # Tenant graph helper: neighbour comparison
    def get_neighbour_payment_summary_for_tenant(self, tenant_id: int):
        """
        Return total payments for the tenant vs average of neighbours
        in the same location and apartment type.
        Used for tenant vs neighbours graph.
        """
        lease = self.get_current_active_lease_for_tenant(tenant_id)
        if not lease:
            return None

        apt = lease.apartment
        loc = apt.location

        neighbour_leases = (
            self.db.query(Lease)
            .join(Apartment, Lease.apartment_id == Apartment.apartment_id)
            .filter(
                Apartment.location_id == loc.location_id,
                Apartment.apartment_type == apt.apartment_type,
            )
            .all()
        )

        lease_ids = [l.lease_id for l in neighbour_leases]
        if not lease_ids:
            return None

        tenant_total = (
            self.db.query(func.sum(Payment.amount_paid))
            .filter(Payment.lease_id == lease.lease_id)
            .scalar()
            or 0
        )

        neighbour_total = (
            self.db.query(func.sum(Payment.amount_paid))
            .filter(Payment.lease_id.in_(lease_ids))
            .scalar()
            or 0
        )

        others_total = max(neighbour_total - tenant_total, 0)
        others_count = max(len(lease_ids) - 1, 1)
        neighbours_avg = others_total / others_count

        return {
            "tenant_total": tenant_total,
            "neighbours_avg": neighbours_avg,
            "location": loc.city,
            "apartment_type": apt.apartment_type,
        }

    # Tenant graph helper: late payments per property
    def get_late_payments_by_property_for_tenant(self, tenant_id: int):
        """
        Return count of late payments per apartment for this tenant.
        Used for late payments per property graph.
        """
        results = (
            self.db.query(
                Apartment.apartment_id,
                func.count(Payment.payment_id).label("late_count"),
            )
            .join(Lease, Lease.lease_id == Payment.lease_id)
            .join(Apartment, Apartment.apartment_id == Lease.apartment_id)
            .filter(
                Lease.tenant_id == tenant_id,
                Payment.is_late == True,
            )
            .group_by(Apartment.apartment_id)
            .all()
        )

        data = []
        for apt_id, late_count in results:
            data.append({"apartment_id": apt_id, "late_count": late_count})
        return data

    # Financial summaries (backend support for reports)
    def get_financial_summary_by_city(self):
        """
        Aggregate collected vs expected per city.
        Used by report_service or directly if needed.
        """
        results = (
            self.db.query(
                Location.city,
                func.sum(Payment.amount_paid).label("collected"),
                func.sum(Payment.amount_due).label("expected"),
            )
            .join(Lease, Lease.lease_id == Payment.lease_id)
            .join(Apartment, Apartment.apartment_id == Lease.apartment_id)
            .join(Location, Location.location_id == Apartment.location_id)
            .group_by(Location.city)
            .all()
        )

        rows = []
        for city, collected, expected in results:
            collected = collected or 0
            expected = expected or 0
            pending = expected - collected
            rows.append(
                {
                    "city": city,
                    "collected": collected,
                    "expected": expected,
                    "pending": pending,
                }
            )
        return rows

    # Tenant "make payment" emulation (card validation stub)
    def validate_card_details(self, card_number: str, expiry: str, cvv: str) -> bool:
        """
        Simple fake card validation for assignment purposes.
        No real processing, just basic format checks.
        """
        if len(card_number.replace(" ", "")) < 12:
            return False
        if len(cvv) not in (3, 4):
            return False
        if "/" not in expiry:
            return False
        return True

    def tenant_make_payment(
        self,
        tenant_id: int,
        lease_id: int,
        amount_due: int,
        amount_paid: int,
        due_date: datetime,
        card_number: str,
        expiry: str,
        cvv: str,
    ) -> Optional[Payment]:
        """
        Tenant-initiated payment from tenant portal.
        - Validates card (emulated)
        - Records payment
        """
        if not self.validate_card_details(card_number, expiry, cvv):
            return None

        return self.record_payment(
            lease_id=lease_id,
            amount_due=amount_due,
            amount_paid=amount_paid,
            due_date=due_date,
        )

    # Cleanup
    def close(self):
        if self.db:
            self.db.close()