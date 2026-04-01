import bcrypt
from sqlalchemy.orm import Session
from database.models import User, TenantAccount, Tenant

# Session object to pass logged-in user info
class UserSession:
    def __init__(self, user_id, username, role, is_tenant, tenant_id=None, location_id=None):
        self.user_id = user_id          # staff user_id or None for tenants
        self.username = username        # login username
        self.role = role                # e.g. "Admin", "FinanceManager", "Tenant"
        self.is_tenant = is_tenant      # True if tenant, False if staff
        self.tenant_id = tenant_id      # tenant_id if tenant
        self.location_id = location_id  


class AuthService:
    def __init__(self, db: Session):
        # Store DB session for queries
        self.db = db

    def authenticate(self, username: str, password: str) -> UserSession | None:
        """
        Try to authenticate as staff first, then as tenant.
        Returns UserSession on success, None on failure.
        """

        staff_session = self._authenticate_staff(username, password)
        if staff_session:
            return staff_session

        tenant_session = self._authenticate_tenant(username, password)
        if tenant_session:
            return tenant_session

        return None

    def _authenticate_staff(self, username: str, password: str) -> UserSession | None:
        # Look up active staff user by username
        user = (
            self.db.query(User)
            .filter(
                User.username == username,
                User.is_active == True 
            )
            .first()
        )

        if not user:
            return None

        # Compare password with stored hash
        if not self._verify_password(password, user.password_hash):
            return None

        # Build session object for staff user
        return UserSession(
            user_id=user.user_id,
            username=user.username,
            role=user.role,
            is_tenant=False,
            tenant_id=None,
            location_id=user.location_id,
        )

    def _authenticate_tenant(self, username: str, password: str) -> UserSession | None:
        # Look up active tenant account by username
        tenant_account = (
            self.db.query(TenantAccount)
            .join(Tenant, TenantAccount.tenant_id == Tenant.tenant_id)
            .filter(
                TenantAccount.username == username,
                TenantAccount.is_active == True, 
                Tenant.is_active == True,         
            )
            .first()
        )

        if not tenant_account:
            return None

        # Compare password with stored hash
        if not self._verify_password(password, tenant_account.password_hash):
            return None

        tenant = tenant_account.tenant

        # Build session object for tenant user
        return UserSession(
            user_id=None, 
            username=tenant_account.username,
            role="Tenant",
            is_tenant=True,
            tenant_id=tenant.tenant_id,
            location_id=tenant.location_id,
        )

    def _verify_password(self, plain_password: str, stored_hash: str) -> bool:
        # Helper to compare plain text password with stored hash
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"),
                stored_hash.encode("utf-8"),
            )
        except Exception:
            return False