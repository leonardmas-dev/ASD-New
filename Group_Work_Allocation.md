This document defines the work split for the team.  
Each one of us owns a complete module (UI + backend + logic), so everyone can work independently with minimal overlap.

---

## Team Structure Overview

| Person    | Module                                | UI Folders                               | Backend Files                                      | Core Responsibilities                                      |
|-----------|----------------------------------------|-------------------------------------------|----------------------------------------------------|------------------------------------------------------------|
| Section 1  | Tenants + Tenant Portal               | `ui/tenants/`, `ui/tenant_portal/`        | `tenant_service.py`, `complaint_service.py`        | Tenant CRUD, tenant portal, graphs, complaints, requests   |
| Section 2  | Apartments + Leases                   | `ui/apartments/`, `ui/leases/`            | `apartment_service.py`, `lease_service.py`         | Apartments, leases, early termination, occupancy           |
| Section 3  | Payments & Billing                    | `ui/payments/`                            | `payment_service.py`, `report_service.py` (finance)| Payments, invoices, late fees, finance workflows           |
| Section 4  | Maintenance + Complaints              | `ui/maintenance/`, `ui/complaints/`       | `maintenance_service.py`, `complaint_service.py`   | Maintenance, staff assignment, complaint resolution        |
| Section 5  | Auth + Users + Reports + Core UI      | `ui/user_management/`, `ui/reports/`, core UI | `auth_service.py`, `user_service.py`, `report_service.py` | Login, roles, navigation, user mgmt, reporting, integration |

---

## Section NO.1 - Allocated to: Leonard Masters – Tenants + Tenant Portal

**UI Folders**

- `ui/tenants/`
- `ui/tenant_portal/`

**UI Files**

- `ui/tenants/tenants_home.py`
- `ui/tenants/add_tenant_page.py`
- `ui/tenants/edit_tenant_page.py`
- `ui/tenants/tenant_list_page.py`
- `ui/tenant_portal/tenant_dashboard.py`
- `ui/tenant_portal/tenant_payments_page.py`
- `ui/tenant_portal/tenant_complaints_page.py`
- `ui/tenant_portal/tenant_maintenance_page.py`
- `ui/tenant_portal/tenant_payment_graphs_page.py`

**Backend Files**

- `backend/tenant_service.py`
- `backend/complaint_service.py` (tenant‑side use)

**Responsibilities**

- Tenant CRUD (Create, Read, Update, Delete)
- Tenant portal dashboard
- View own payment history
- Submit complaints
- Submit maintenance requests
- Payment history graphs
- “Tenant vs neighbours” style graphs (if implemented)
- Work with Person 2 to link tenants and leases

---

## Section NO.2 - Allocated to: Thierno Batiga – Apartments + Leases

**UI Folders**

- `ui/apartments/`
- `ui/leases/`

**UI Files**

- `ui/apartments/apartments_home.py`
- `ui/apartments/add_apartment_page.py`
- `ui/apartments/edit_apartment_page.py`
- `ui/apartments/apartment_list_page.py`
- `ui/leases/leases_home.py`
- `ui/leases/add_lease_page.py`
- `ui/leases/edit_lease_page.py`
- `ui/leases/lease_list_page.py`

**Backend Files**

- `backend/apartment_service.py`
- `backend/lease_service.py`

**Responsibilities**

- Apartment CRUD (Create, Read, Update, Delete)
- Apartment availability status
- Lease creation and editing
- Early termination logic (1 month notice + 5% penalty)
- Tracking occupancy
- Linking apartments ↔ tenants (with Person 1)

---

## Section NO.3 - Allocated to: Yaseen Sassi – Payments & Billing

**UI Folder**

- `ui/payments/`

**UI Files**

- `ui/payments/payments_home.py`
- `ui/payments/record_payment_page.py`
- `ui/payments/payment_history_page.py`

**Backend Files**

- `backend/payment_service.py`
- `backend/report_service.py` (financial reporting parts)

**Responsibilities**

- Record payments
- Generate invoices (if implemented here)
- Detect and mark late payments
- Apply late fees
- Finance manager workflows
- Payment history logic
- Financial summaries (collected vs pending)
- Integrate with tenant portal payment views (Person 1)

---

## Section NO.4 - Allocated to: Ishak Askar – Maintenance + Complaints

**UI Folders**

- `ui/maintenance/`
- `ui/complaints/`

**UI Files**

- `ui/maintenance/maintenance_home.py`
- `ui/maintenance/create_request_page.py`
- `ui/maintenance/update_request_page.py`
- `ui/maintenance/maintenance_list_page.py`
- `ui/complaints/complaints_home.py`
- `ui/complaints/add_complaint_page.py`
- `ui/complaints/complaint_list_page.py`

**Backend Files**

- `backend/maintenance_service.py`
- `backend/complaint_service.py` (admin‑side use)

**Responsibilities**

- Maintenance request creation and updates
- Assigning maintenance staff to requests
- Logging time taken and cost
- Tracking maintenance status and history
- Admin‑side complaint handling and resolution
- Maintenance cost reporting (with Person 5)
- Linking maintenance to tenants, leases, and apartments

---

## Section NO.5 - Allocated to: Yaseen Sassi – Folder/File Structures + Database + Authentication + User Management and access control + Reports module + Core UI and Navigation

**UI Folders**

- `ui/user_management/`
- `ui/reports/`

**UI Files**

- `ui/user_management/users_home.py`
- `ui/user_management/add_user_page.py`
- `ui/user_management/edit_user_page.py`
- `ui/reports/reports_home.py`
- `ui/reports/occupancy_report_page.py`
- `ui/reports/financial_report_page.py`
- `ui/reports/maintenance_report_page.py`

**Core UI Files**

- `ui/main_window.py`
- `ui/navigation.py`
- `ui/login_page.py`
- `ui/home_page.py`

**Backend Files**

- `backend/auth_service.py`
- `backend/user_service.py`
- `backend/report_service.py` (all reporting)

**Utils**

- `utils/config.py`
- `utils/validators.py`
- `utils/helpers.py`

**Responsibilities**

- Creating folder a complete and file structure for the app
- Database creation using SQL Alchemy
- Login system (staff + tenants)
- Authentication and password handling
- Role‑based access control
- Navigation and home page structure
- Home dashboard for staff
- User (staff) management
- All reporting (occupancy, financial, maintenance)
- Shared helpers and configuration
- Ensuring all modules integrate cleanly

---

## Workflow & Github

- The full project structure is shared via the GitHub repo.
- Each person works **only** inside their assigned folders and files.
- Everyone uses `git pull` to stay up to date and `git push` to share changes.
- Because modules are separated between us, integration at the end should be straightforward.