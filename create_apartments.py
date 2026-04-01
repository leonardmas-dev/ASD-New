# Student: Yaseen Sassi     StudentID: 24023127

from database.session import get_session
from database.models import Apartment, Location

def seed_apartments():
    db = get_session()
# Here I just made some apartments to pre populate database
    locations = db.query(Location).all()
    if not locations:
        print("ERROR: No locations found. Run create_locations.py first.")
        return

    apartment_templates = [
        # type, rooms, rent
        ("Studio", 1, 650),
        ("Studio", 1, 700),
        ("Studio", 1, 750),

        ("1-Bed", 2, 900),
        ("1-Bed", 2, 950),
        ("1-Bed", 2, 1000),
        ("1-Bed", 2, 1100),

        ("2-Bed", 3, 1200),
        ("2-Bed", 3, 1300),
        ("2-Bed", 3, 1400),
        ("2-Bed", 3, 1500),

        ("3-Bed", 4, 1600),
        ("3-Bed", 4, 1700),
        ("3-Bed", 4, 1800),

        ("4-Bed", 5, 2000),
        ("4-Bed", 5, 2200),

        ("Penthouse", 4, 3000),
        ("Penthouse", 5, 3500),

        ("Accessible Unit", 2, 950),
        ("Luxury Unit", 3, 2500),
        ("Luxury Unit", 4, 2800),
    ]

    total_inserted = 0

    for location in locations:
        print(f"\nSeeding apartments for {location.city}...")

        floor_counter = 1

        for apt_type, rooms, rent in apartment_templates:
            # Creates 2 of each type per location for variety
            for _ in range(2):
                apartment = Apartment(
                    location_id=location.location_id,
                    apartment_type=apt_type,
                    monthly_rent=rent,
                    num_rooms=rooms,
                    floor_number=floor_counter,
                    is_available=True,
                    is_active=True
                )

                db.add(apartment)
                total_inserted += 1

                floor_counter += 1
                if floor_counter > 12:
                    floor_counter = 1

    db.commit()
    db.close()

    print(f"\n=== Apartment Seeding Complete ===")
    print(f"Total apartments inserted: {total_inserted}")


if __name__ == "__main__":
    seed_apartments()