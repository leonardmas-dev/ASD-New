from database.models import Tenant
from database.session import get_session

def fetch_tenants():
    with get_session() as session:
        return session.query(Tenant).all()
    
# tenant_service allows less code reuse as this file can be imported to all files