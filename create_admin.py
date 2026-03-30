import bcrypt
from database.session import get_session
from database.models import User

def create_admin():
    db = get_session()

    password = "admin"
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    admin = User(
        first_name="System",
        last_name="Admin",
        email="admin@paragonapartments.com",
        phone="0000000000",
        username="admin",
        password_hash=hashed,
        role="Admin",
        location_id=1,  # adjust if needed
        is_active=True
    )

    db.add(admin)
    db.commit()
    db.close()

    print("Admin created: username=admin, password=admin")

if __name__ == "__main__":
    create_admin()