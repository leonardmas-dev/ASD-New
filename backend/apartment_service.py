import mysql.connector
from tkinter import messagebox

# 1. Connection Helper
def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",          # Update with your MySQL user
            password="1105",  # Update with your MySQL password
            database="apartment_management"    # Update with your DB name
        )
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# 2. Create (Add Apartment)
def add_apartment(location, apt_type, rent, rooms):
    db = get_db_connection()
    if not db: return False
    
    cursor = db.cursor()
    query = "INSERT INTO apartments (location, type, rent, rooms, status) VALUES (%s, %s, %s, %s, 'Available')"
    try:
        cursor.execute(query, (location, apt_type, rent, rooms))
        db.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        db.close()

# 3. Read (Fetch all for the Treeview)
def get_all_apartments():
    db = get_db_connection()
    if not db: return []
    
    cursor = db.cursor(dictionary=True) # Returns data as a dictionary
    cursor.execute("SELECT * FROM apartment")
    results = cursor.fetchall()
    db.close()
    return results

# 4. Update & Delete (The rest of your CRUD)
# You will add update_apartment() and delete_apartment() here