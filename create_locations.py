from database.session import get_session
from database.models import Location

def create_locations():
    db = get_session()
# Here I just made some locations to pre populate database
    locations = [
        Location(
            name="Bristol Office",
            city="Bristol",
            postcode="BS1 1AA",
            phone="0117 000 0000",
            is_active=True
        ),
        Location(
            name="Cardiff Office",
            city="Cardiff",
            postcode="CF10 1AA",
            phone="0292 000 0000",
            is_active=True
        ),
        Location(
            name="London Office",
            city="London",
            postcode="EC1A 1AA",
            phone="0207 000 0000",
            is_active=True
        ),
        Location(
            name="Manchester Office",
            city="Manchester",
            postcode="M1 1AA",
            phone="0161 000 0000",
            is_active=True
        ),
    ]

    db.add_all(locations)
    db.commit()
    db.close()

    print("Locations inserted successfully.")

if __name__ == "__main__":
    create_locations()