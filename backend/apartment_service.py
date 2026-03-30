import mysql.connector

# 1. Connection Helper
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1105", 
            database="apartment_management"
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 2. Create (Add Apartment)
def add_apartment(location_name, apt_type, rent, rooms):
    db = get_db_connection()
    if not db: return False
    
    # Map city names to the IDs in my location table
    location_map = {"Bristol": 1, "Cardiff": 2, "London": 3, "Manchester": 4}
    loc_id = location_map.get(location_name, 1)

    cursor = db.cursor()
    # Match my exact DB columns:
    query = """INSERT INTO apartment 
               (location_id, apartment_type, monthly_rent, num_rooms, is_available) 
               VALUES (%s, %s, %s, %s, 1)"""
    try:
        cursor.execute(query, (loc_id, apt_type, float(rent), int(rooms)))
        db.commit()
        return True
    except Exception as e:
        print(f"Insert Error: {e}")
        return False
    finally:
        db.close()

# 3. Read (Fetch all for the Treeview)
def get_all_apartments():
    db = get_db_connection()
    if not db: return []
    
    cursor = db.cursor(dictionary=True) 
    cursor.execute("SELECT * FROM apartment")
    results = cursor.fetchall()
    db.close()
    return results

# 4. Read Single (For the Edit Page)
def get_apartment_by_id(apt_id):
    db = get_db_connection()
    if not db: return None
    
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM apartment WHERE apartment_id = %s", (apt_id,))
    result = cursor.fetchone()
    db.close()
    return result

# 5. Update
def update_apartment(apt_id, location_name, apt_type, rent, status):
    db = get_db_connection()
    if not db: return False
    
    location_map = {"Bristol": 1, "Cardiff": 2, "London": 3, "Manchester": 4}
    loc_id = location_map.get(location_name, 1)
    # 1 for Available, 0 for Occupied/Maintenance
    is_avail = 1 if status == "Available" else 0

    try:
        cursor = db.cursor()
        query = """UPDATE apartment 
                   SET location_id=%s, apartment_type=%s, monthly_rent=%s, is_available=%s 
                   WHERE apartment_id=%s"""
        cursor.execute(query, (loc_id, apt_type, float(rent), is_avail, apt_id))
        db.commit()
        return True
    except Exception as e:
        print(f"Update Error: {e}")
        return False
    finally:
        db.close()

# 6. Delete
def delete_apartment(apt_id):
    db = get_db_connection()
    if not db: return False
    try:
        cursor = db.cursor()
        cursor.execute("DELETE FROM apartment WHERE apartment_id=%s", (apt_id,))
        db.commit()
        return True
    except Exception as e:
        print(f"Delete Error: {e}")
        return False
    finally:
        db.close()
def get_available_apartments():
    """Fetches only apartments where is_available is 1"""
    db = get_db_connection()
    if not db: return []
    
    try:
        cursor = db.cursor(dictionary=True)
        #only want the ones that can actually be booked
        query = "SELECT apartment_id, apartment_type FROM apartment WHERE is_available = 1"
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(f"Fetch Available Error: {e}")
        return []
    finally:
        db.close()