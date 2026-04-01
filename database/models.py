# Student: Yaseen Sassi     StudentID: 24023127

from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()


# 1. Location

class Location(Base):
    __tablename__ = "location"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    postcode = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    tenants = relationship("Tenant", back_populates="location")
    users = relationship("User", back_populates="location")
    apartments = relationship("Apartment", back_populates="location")



# 2. Tenant

class Tenant(Base):
    __tablename__ = "tenant"

    tenant_id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("location.location_id"), nullable=False)

    ni_number = Column(String(50), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    occupation = Column(String(255), nullable=True)
    references_text = Column(String(500), nullable=True)
    apartment_requirements = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    location = relationship("Location", back_populates="tenants")
    tenant_account = relationship("TenantAccount", back_populates="tenant", uselist=False)

    leases = relationship("Lease", back_populates="tenant")
    complaints = relationship("Complaint", back_populates="tenant")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="tenant")



# 3. User (Staff)

class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("location.location_id"), nullable=False)

    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(50), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    location = relationship("Location", back_populates="users")
    staff_assignments = relationship("MaintenanceStaffAssignment", back_populates="user")



# 4. TenantAccount (1:1)

class TenantAccount(Base):
    __tablename__ = "tenant_account"

    tenant_account_id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey("tenant.tenant_id"), nullable=False, unique=True)

    username = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    tenant = relationship("Tenant", back_populates="tenant_account")


# 5. Apartment
class Apartment(Base):
    __tablename__ = "apartment"

    apartment_id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("location.location_id"), nullable=False)

    apartment_type = Column(String(255), nullable=False)
    monthly_rent = Column(Integer, nullable=False)
    num_rooms = Column(Integer, nullable=False)
    floor_number = Column(Integer, nullable=False)
    is_available = Column(Boolean, default=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    location = relationship("Location", back_populates="apartments")
    leases = relationship("Lease", back_populates="apartment")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="apartment")


# 6. Lease

class Lease(Base):
    __tablename__ = "lease"

    lease_id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey("tenant.tenant_id"), nullable=False)
    apartment_id = Column(Integer, ForeignKey("apartment.apartment_id"), nullable=False)

    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    monthly_rent = Column(Integer, nullable=False)
    deposit_amount = Column(Integer, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    tenant = relationship("Tenant", back_populates="leases")
    apartment = relationship("Apartment", back_populates="leases")

    payments = relationship("Payment", back_populates="lease")
    invoices = relationship("Invoice", back_populates="lease")
    complaints = relationship("Complaint", back_populates="lease")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="lease")



# 7. Payment

class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(Integer, primary_key=True, autoincrement=True)
    lease_id = Column(Integer, ForeignKey("lease.lease_id"), nullable=False)

    amount_due = Column(Integer, nullable=False)
    amount_paid = Column(Integer, nullable=False)
    due_date = Column(DateTime, nullable=False)
    payment_date = Column(DateTime, nullable=True)
    is_late = Column(Boolean, default=False, nullable=False)
    late_fee = Column(Integer, nullable=True)
    status = Column(String(100), nullable=False)

    lease = relationship("Lease", back_populates="payments")



# 8. Invoice

class Invoice(Base):
    __tablename__ = "invoice"

    invoice_id = Column(Integer, primary_key=True, autoincrement=True)
    lease_id = Column(Integer, ForeignKey("lease.lease_id"), nullable=False)

    amount_due = Column(Integer, nullable=False)
    issue_date = Column(DateTime, nullable=False)
    due_date = Column(DateTime, nullable=False)
    status = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    is_late = Column(Boolean, default=False, nullable=False)

    lease = relationship("Lease", back_populates="invoices")



# 9. Complaint
class Complaint(Base):
    __tablename__ = "complaint"

    complaint_id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey("tenant.tenant_id"), nullable=False)
    lease_id = Column(Integer, ForeignKey("lease.lease_id"), nullable=False)

    description = Column(String(500), nullable=False)
    submitted_at = Column(DateTime, nullable=False)
    status = Column(String(100), nullable=False)
    resolved_at = Column(DateTime, nullable=True)
    resolution_notes = Column(String(500), nullable=True)

    tenant = relationship("Tenant", back_populates="complaints")
    lease = relationship("Lease", back_populates="complaints")



# 10. MaintenanceRequest
class MaintenanceRequest(Base):
    __tablename__ = "maintenance_request"

    maintenance_request_id = Column(Integer, primary_key=True, autoincrement=True)
    tenant_id = Column(Integer, ForeignKey("tenant.tenant_id"), nullable=False)
    apartment_id = Column(Integer, ForeignKey("apartment.apartment_id"), nullable=False)
    lease_id = Column(Integer, ForeignKey("lease.lease_id"), nullable=False)

    description = Column(String(500), nullable=False)
    priority = Column(String(100), nullable=False)
    status = Column(String(100), nullable=False)
    submitted_at = Column(DateTime, nullable=False)
    scheduled_date = Column(DateTime, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    time_taken_hours = Column(Integer, nullable=True)
    cost = Column(Integer, nullable=True)
    notes = Column(String(500), nullable=True)

    tenant = relationship("Tenant", back_populates="maintenance_requests")
    apartment = relationship("Apartment", back_populates="maintenance_requests")
    lease = relationship("Lease", back_populates="maintenance_requests")

    staff_assignments = relationship("MaintenanceStaffAssignment", back_populates="maintenance_request")


# 11. MaintenanceStaffAssignment
class MaintenanceStaffAssignment(Base):
    __tablename__ = "maintenance_staff_assignment"

    assignment_id = Column(Integer, primary_key=True, autoincrement=True)
    maintenance_request_id = Column(Integer, ForeignKey("maintenance_request.maintenance_request_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)

    assigned_at = Column(DateTime, nullable=False)
    notes = Column(String(500), nullable=True)

    maintenance_request = relationship("MaintenanceRequest", back_populates="staff_assignments")
    user = relationship("User", back_populates="staff_assignments")