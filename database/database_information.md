# A brief overview of the database covering all entities and attributes and their purpose:

---

## 1. Entity: Location

**Purpose:**  
Represents each physical building or apartment complex managed by the system. All tenants, staff, and apartments belong to a specific location.

**Attributes / Fields:**

- **location_id** — Primary key; unique ID for each location.  
- **name** — Name of the building or complex.  
- **city** — City where the location is situated.  
- **postcode** — Postal/ZIP code for the location.  
- **phone** — Main contact phone number for the location or office.  
- **is_active** — Indicates whether the location is currently active in the system.  

---

## 2. Entity: User (Stores Staff Info)

**Purpose:**  
Represents staff members working at a location, including managers, maintenance staff, and administrative staff. Staff can log in and be assigned to maintenance tasks.

**Attributes / Fields:**

- **user_id** — Primary key; unique ID for each staff member.  
- **location_id** — FK → `location.location_id`; staff member’s assigned location.  
- **first_name** — Staff member’s first name.  
- **last_name** — Staff member’s last name.  
- **email** — Staff email address.  
- **phone** — Staff contact number.  
- **username** — Unique login username.  
- **password_hash** — Hashed password for authentication.  
- **role** — Staff role (e.g., “Manager”, “Maintenance”, “Admin”).  
- **is_active** — Indicates whether the staff account is active.  

---

## 3. Entity: Tenant

**Purpose:**  
Represents individuals renting apartments within a location. Stores personal details, screening information, and preferences relevant to tenancy.

**Attributes / Fields:**

- **tenant_id** — Primary key; unique ID for each tenant.  
- **location_id** — FK → `location.location_id`; identifies which location the tenant belongs to.  
- **ni_number** — National Insurance number used for identity verification and background checks.  
- **first_name** — Tenant’s first name.  
- **last_name** — Tenant’s last name.  
- **phone** — Tenant’s contact number.  
- **email** — Tenant’s email address.  
- **occupation** — Tenant’s job or employment status.  
- **references_text** — Free-text field storing references or screening notes (e.g., previous landlord reference, employer reference, background check notes).  
- **apartment_requirements** — Tenant’s preferences or needs (e.g., “2 bedrooms”, “ground floor”, “pet-friendly”).  
- **created_at** — Timestamp indicating when the tenant record was created.  
- **is_active** — Indicates whether the tenant is currently active (e.g., still renting or recently moved out).

---

## 4. Entity: TenantAccount (1:1 Relationship With Tenant)

**Purpose:**  
Stores login credentials for tenants to access the tenant portal. Each tenant has exactly one account.

**Attributes / Fields:**

- **tenant_account_id** — Primary key; unique ID for each tenant account.  
- **tenant_id** — FK → `tenant.tenant_id`; unique, enforcing a 1:1 relationship.  
- **username** — Unique tenant login username.  
- **password_hash** — Hashed password for tenant authentication.  
- **is_active** — Indicates whether the tenant account is active.  

---

## 5. Entity: Apartment

**Purpose:**  
Represents individual apartment units within a location. Leases and maintenance requests are tied to apartments.

**Attributes / Fields:**

- **apartment_id** — Primary key; unique ID for each apartment.  
- **location_id** — FK → `location.location_id`; which location the apartment belongs to.  
- **apartment_type** — Type of apartment (e.g., “Studio”, “1 Bedroom”, “2 Bedroom”).  
- **monthly_rent** — Standard monthly rent for the apartment.  
- **num_rooms** — Number of rooms in the apartment.  
- **floor_number** — Floor level where the apartment is located.  
- **is_available** — Indicates whether the apartment is currently available for rent.  
- **is_active** — Indicates whether the apartment is active in the system.  

---

## 6. Entity: Lease

**Purpose:**  
Represents a rental agreement between a tenant and an apartment over a defined period.

**Attributes / Fields:**

- **lease_id** — Primary key; unique ID for each lease.  
- **tenant_id** — FK → `tenant.tenant_id`; tenant who signed the lease.  
- **apartment_id** — FK → `apartment.apartment_id`; apartment being leased.  
- **start_date** — Date when the lease begins.  
- **end_date** — Date when the lease ends.  
- **monthly_rent** — Monthly rent agreed in the lease.  
- **deposit_amount** — Security deposit amount paid by the tenant.  
- **is_active** — Indicates whether the lease is currently active.  

---

## 7. Entity: Payment

**Purpose:**  
Records payments made by tenants toward their lease obligations.

**Attributes / Fields:**

- **payment_id** — Primary key; unique ID for each payment.  
- **lease_id** — FK → `lease.lease_id`; lease the payment relates to.  
- **amount_due** — Amount that was due for the payment period.  
- **amount_paid** — Amount actually paid by the tenant.  
- **due_date** — Date the payment was due.  
- **payment_date** — Date the payment was made.  
- **is_late** — Indicates whether the payment was late.  
- **late_fee** — Additional fee charged for late payment.  
- **status** — Payment status (e.g., “Paid”, “Unpaid”, “Late”).  

---

## 8. Entity: Invoice

**Purpose:**  
Represents invoices issued to tenants for rent or other charges.

**Attributes / Fields:**

- **invoice_id** — Primary key; unique ID for each invoice.  
- **lease_id** — FK → `lease.lease_id`; lease the invoice is associated with.  
- **amount_due** — Amount billed on the invoice.  
- **issue_date** — Date the invoice was created.  
- **due_date** — Date payment is due.  
- **status** — Invoice status (e.g., “Paid”, “Unpaid”, “Overdue”).  
- **description** — Optional description or notes about the invoice.  
- **is_late** — Indicates whether the invoice is overdue.  

---

## 9. Entity: Complaint

**Purpose:**  
Allows tenants to submit complaints related to their lease, apartment, or living conditions.

**Attributes / Fields:**

- **complaint_id** — Primary key; unique ID for each complaint.  
- **tenant_id** — FK → `tenant.tenant_id`; tenant who submitted the complaint.  
- **lease_id** — FK → `lease.lease_id`; lease associated with the complaint.  
- **description** — Detailed description of the complaint.  
- **submitted_at** — Timestamp when the complaint was submitted.  
- **status** — Complaint status (e.g., “Open”, “In Progress”, “Resolved”).  
- **resolved_at** — Timestamp when the complaint was resolved.  
- **resolution_notes** — Notes describing how the complaint was resolved.  

---

## 10. Entity: MaintenanceRequest

**Purpose:**  
Represents maintenance issues reported by tenants. Requests can be assigned to staff and tracked through completion.

**Attributes / Fields:**

- **maintenance_request_id** — Primary key; unique ID for each request.  
- **tenant_id** — FK → `tenant.tenant_id`; tenant who submitted the request.  
- **apartment_id** — FK → `apartment.apartment_id`; apartment where the issue occurred.  
- **lease_id** — FK → `lease.lease_id`; lease associated with the request.  
- **description** — Description of the maintenance issue.  
- **priority** — Priority level (e.g., “Low”, “Medium”, “High”).  
- **status** — Current status (e.g., “Pending”, “In Progress”, “Completed”).  
- **submitted_at** — Timestamp when the request was submitted.  
- **scheduled_date** — Date maintenance is scheduled to occur.  
- **resolved_at** — Date the issue was resolved.  
- **time_taken_hours** — Total time spent resolving the issue.  
- **cost** — Cost of the maintenance work.  
- **notes** — Additional notes about the request or work performed.  

---

## 11. Entity: MaintenanceStaffAssignment

**Purpose:**  
Join table linking staff members to maintenance requests, enabling many-to-many assignment of staff to tasks.

**Attributes / Fields:**

- **assignment_id** — Primary key; unique ID for each assignment.  
- **maintenance_request_id** — FK → `maintenance_request.maintenance_request_id`; request being handled.  
- **user_id** — FK → `user.user_id`; staff member assigned to the request.  
- **assigned_at** — Timestamp when the staff member was assigned.  
- **notes** — Optional notes about the assignment or work done.  

---