from database.models import Tenant
from database.session import get_session
from sqlalchemy.orm import joinedload

def fetch_tenants():
    with get_session() as session:
        return session.query(Tenant).all()
    
# tenant_service allows less code reuse as this file can be imported to all files

class TenantService:

    @staticmethod
    def get_all_tenants():
        db = get_session()
        tenants = (
            db.query(Tenant)
            .options(joinedload(Tenant.location))
            .all()
        )
        db.close()
        return tenants

    @staticmethod
    def get_tenant_by_id(tenant_id):
        db = get_session()
        tenant = (
            db.query(Tenant)
            .options(joinedload(Tenant.location))
            .filter(Tenant.tenant_id == tenant_id)
            .first()
        )
        db.close()
        return tenant

    @staticmethod
    def ni_number_exists(ni_number):
        db = get_session()
        exists = db.query(Tenant).filter(Tenant.ni_number == ni_number).first()
        db.close()
        return exists is not None

    @staticmethod
    def create_tenant(data):
        db = get_session()
        new_tenant = Tenant(
            first_name = data["first_name"],
            last_name = data["last_name"],
            email = data["email"],
            phone = data["phone"],
            ni_number = data["ni_number"],
            occupation = data.get("occupation"),
            references_text = data.get("references_text"),
            apartment_requirements = data.get("apartment_requirements"),
            location_id = data["location_id"],
            is_active = True
        )
        db.add(new_tenant)
        db.commit()
        db.close()

    @staticmethod
    def update_tenant(tenant_id, data):
        db = get_session()
        tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
        if not tenant:
            db.close()
            return
        tenant.first_name = data["first_name"],
        tenant.last_name = data["last_name"],
        tenant.email = data["email"],
        tenant.phone = data["phone"],
        tenant.ni_number = data["ni_number"],
        tenant.occupation = data.get("occupation"),
        tenant.references_text = data.get("references_text"),
        tenant.apartment_requirements = data.get("apartment_requirements"),
        tenant.location_id = data["location_id"],
        
        db.commit()
        db.close()

    @staticmethod
    def deactivate_tenant(tenant_id):
        db = get_session()
        tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
        if tenant:
            tenant.is_active = False
            db.commit()
        db.close()

    @staticmethod
    def activate_tenant(tenant_id):
        db = get_session()
        tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
        if tenant:
            tenant.is_active = True
            db.commit()
        db.close()