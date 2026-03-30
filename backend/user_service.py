import bcrypt
from database.session import get_session
from database.models import User
from sqlalchemy.orm import joinedload

class UserService:

    @staticmethod
    def get_all_users():
        db = get_session()
        users = (
            db.query(User)
            .options(joinedload(User.location))
            .all()
        )
        db.close()
        return users

    @staticmethod
    def get_user_by_id(user_id):
        db = get_session()
        user = (
            db.query(User)
            .options(joinedload(User.location))
            .filter(User.user_id == user_id)
            .first()
        )
        db.close()
        return user

    @staticmethod
    def username_exists(username):
        db = get_session()
        exists = db.query(User).filter(User.username == username).first()
        db.close()
        return exists is not None

    @staticmethod
    def create_user(data):
        db = get_session()

        # hash password using bcrypt
        hashed_pw = bcrypt.hashpw(
            data["password"].encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            phone=data["phone"],
            username=data["username"],
            password_hash=hashed_pw,
            role=data["role"],
            location_id=data["location_id"],
            is_active=True
        )

        db.add(new_user)
        db.commit()
        db.close()

    @staticmethod
    def update_user(user_id, data):
        db = get_session()
        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            db.close()
            return

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        user.phone = data["phone"]
        user.role = data["role"]
        user.location_id = data["location_id"]

        # update password only if provided
        if data.get("password"):
            hashed_pw = bcrypt.hashpw(
                data["password"].encode("utf-8"),
                bcrypt.gensalt()
            ).decode("utf-8")
            user.password_hash = hashed_pw

        db.commit()
        db.close()

    @staticmethod
    def deactivate_user(user_id):
        db = get_session()
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.is_active = False
            db.commit()
        db.close()

    @staticmethod
    def activate_user(user_id):
        db = get_session()
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.is_active = True
            db.commit()
        db.close()