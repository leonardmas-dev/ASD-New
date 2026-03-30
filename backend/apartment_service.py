from typing import List, Dict, Optional

from sqlalchemy.orm import Session
from sqlalchemy import or_

from database.models import Apartment, Location


class ApartmentService:
    def __init__(self, db: Session):
        # store db session
        self.db = db

    # resolve location by city or name
    def _get_location_id(self, location_name: str) -> Optional[int]:
        if not location_name:
            return None
        loc = (
            self.db.query(Location)
            .filter(
                or_(
                    Location.city == location_name,
                    Location.name == location_name,
                )
            )
            .first()
        )
        return loc.location_id if loc else None

    # create apartment
    def add_apartment(
        self,
        location_name: str,
        apt_type: str,
        rent: str,
        rooms: str,
        floor: str,
    ) -> bool:
        try:
            location_id = self._get_location_id(location_name)
            if location_id is None:
                return False

            monthly_rent = int(float(rent))
            num_rooms = int(rooms)
            floor_number = int(floor or 1)

            apt = Apartment(
                location_id=location_id,
                apartment_type=apt_type or "Unknown",
                monthly_rent=monthly_rent,
                num_rooms=num_rooms,
                floor_number=floor_number,
                is_available=True,
                is_active=True,
            )
            self.db.add(apt)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Insert Error: {e}")
            return False

    # list all active apartments
    def get_all_apartments(self) -> List[Dict]:
        try:
            apartments = (
                self.db.query(Apartment)
                .filter(Apartment.is_active == True)
                .all()
            )
            data: List[Dict] = []
            for a in apartments:
                data.append(
                    {
                        "apartment_id": a.apartment_id,
                        "location_id": a.location_id,
                        "apartment_type": a.apartment_type,
                        "monthly_rent": a.monthly_rent,
                        "num_rooms": a.num_rooms,
                        "is_available": 1 if a.is_available else 0,
                    }
                )
            return data
        except Exception as e:
            print(f"Fetch Error: {e}")
            return []

    # single apartment by id
    def get_apartment_by_id(self, apt_id: int) -> Optional[Dict]:
        try:
            a = (
                self.db.query(Apartment)
                .filter(
                    Apartment.apartment_id == apt_id,
                    Apartment.is_active == True,
                )
                .first()
            )
            if not a:
                return None
            return {
                "apartment_id": a.apartment_id,
                "location_id": a.location_id,
                "apartment_type": a.apartment_type,
                "monthly_rent": a.monthly_rent,
                "num_rooms": a.num_rooms,
                "floor_number": a.floor_number,
                "is_available": 1 if a.is_available else 0,
            }
        except Exception as e:
            print(f"Fetch One Error: {e}")
            return None

    # update apartment core fields + availability
    def update_apartment(
        self,
        apt_id: int,
        location_name: str,
        apt_type: str,
        rent: str,
        status: str,
    ) -> bool:
        try:
            a = (
                self.db.query(Apartment)
                .filter(
                    Apartment.apartment_id == apt_id,
                    Apartment.is_active == True,
                )
                .first()
            )
            if not a:
                return False

            location_id = self._get_location_id(location_name) or a.location_id
            a.location_id = location_id
            a.apartment_type = apt_type or a.apartment_type
            a.monthly_rent = int(float(rent)) if rent else a.monthly_rent

            # status → availability flag
            if status == "Available":
                a.is_available = True
            else:
                a.is_available = False

            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Update Error: {e}")
            return False

    # hard delete (matches original behaviour)
    def delete_apartment(self, apt_id: int) -> bool:
        try:
            a = (
                self.db.query(Apartment)
                .filter(Apartment.apartment_id == apt_id)
                .first()
            )
            if not a:
                return False

            self.db.delete(a)
            self.db.commit()
            return True
        except Exception as e:
            self.db.rollback()
            print(f"Delete Error: {e}")
            return False

    # list only available apartments for leasing
    def get_available_apartments(self) -> List[Dict]:
        try:
            apartments = (
                self.db.query(Apartment)
                .filter(
                    Apartment.is_active == True,
                    Apartment.is_available == True,
                )
                .all()
            )
            return [
                {
                    "apartment_id": a.apartment_id,
                    "apartment_type": a.apartment_type,
                }
                for a in apartments
            ]
        except Exception as e:
            print(f"Fetch Available Error: {e}")
            return []