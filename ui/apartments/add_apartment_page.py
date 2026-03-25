import mysql.connector
from tkinter import messagebox

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",          # Update this to your MySQL username
            password="1105",  # Update this to your MySQL password
            database="apartment_management" 
        )
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None

def add_apartment(location_name, apt_type, rent, rooms, floor=1):
    """
    Saves a new apartment record to the 'apartment' table.
    """
    # 1. Map City Names to ID
    location_map = {
        "Bristol": 1,
        "Cardiff": 2,
        "London": 3,
        "Manchester": 4
    }
    
    loc_id = location_map.get(location_name, 1)

    db = get_db_connection()
    if not db:
        return False 

    cursor = db.cursor()

    # 2. Match your EXACT MySQL columns from the screenshot
    query = """
        INSERT INTO apartment 
        (location_id, apartment_type, monthly_rent, num_rooms, floor_number, is_available, is_active) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    values = (loc_id, apt_type, float(rent), int(rooms), int(floor), 1, 1)

    try:
        cursor.execute(query, values)
        db.commit()
        print(f"✅ Successfully inserted apartment at location {loc_id}")
        return True
    except mysql.connector.Error as err:
        print(f"❌ SQL Error: {err}")
        return False
    finally:
        cursor.close()
        db.close()

def get_all_apartments():
    """Fetches all apartments to display in the Treeview list"""
    db = get_db_connection()
    if not db: return []
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM apartment")
    results = cursor.fetchall()
    db.close()
    return results

# --- THE TEST BLOCK ---
# This code only runs if you play this file directly
if __name__ == "__main__":
    print("--- STARTING DATABASE TEST ---")
    
    # Let's try to add one test apartment automatically
    test_result = add_apartment(
        location_name="Bristol", 
        apt_type="2-Bedroom", 
        rent=1200.00, 
        rooms=3, 
        floor=2
    )
    
    if test_result:
        print("Test 1: Success! Check your MySQL Workbench table.")
    else:
        print("Test 1: Failed. Read the error message above.")
        
    # Let's see what is currently in the database
    data = get_all_apartments()
    print(f"Total apartments in DB: {len(data)}")
    for row in data:
        print(row)