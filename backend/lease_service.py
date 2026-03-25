import mysql.connector
from datetime import datetime, timedelta

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="1105", 
            database="apartment_management"
        )
    except mysql.connector.Error as err:
        print(f"Connection Error: {err}")
        return None

# 1. Create a New Lease
def create_lease(tenant_id, apartment_id, start_date, duration_months, rent, deposit):
    db = get_db_connection()
    if not db: return False
    
    try:
        cursor = db.cursor()
        # Calculate end date
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = start_dt + timedelta(days=int(duration_months) * 30)
        
        query = """INSERT INTO lease 
                   (tenant_id, apartment_id, start_date, monthly_rent, end_date, deposit_amount, is_active) 
                   VALUES (%s, %s, %s, %s, %s, %s, 1)"""
        
        values = (tenant_id, apartment_id, start_date, float(rent), end_dt.date(), float(deposit))
        cursor.execute(query, values)
        
        # STATUS FLIP: Mark apartment as occupied
        cursor.execute("UPDATE apartment SET is_available = 0 WHERE apartment_id = %s", (apartment_id,))
        
        db.commit()
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        db.close()

# 2. Get All Leases (For the UI Table)
def get_all_leases():
    db = get_db_connection()
    if not db: return []
    
    try:
        cursor = db.cursor(dictionary=True)
        # We join with tenant to get names instead of just IDs
        query = """
            SELECT l.*, t.first_name, t.last_name 
            FROM lease l
            JOIN tenant t ON l.tenant_id = t.tenant_id
            WHERE l.is_active = 1
        """
        cursor.execute(query)
        return cursor.fetchall()
    finally:
        db.close()

# 3. Terminate Lease & Calculate Penalty
def terminate_lease(lease_id, apartment_id):
    db = get_db_connection()
    if not db: return None
    
    try:
        cursor = db.cursor(dictionary=True)
        
        # 1. Fetch lease details to calculate penalty
        cursor.execute("SELECT monthly_rent FROM lease WHERE lease_id = %s", (lease_id,))
        lease = cursor.fetchone()
        
        if not lease:
            return None

        # 2. Calculate Penalty (5% of monthly rent as per Paragon rules)
        penalty = float(lease['monthly_rent']) * 0.05
        
        # 3. Mark lease as inactive
        cursor.execute("UPDATE lease SET is_active = 0 WHERE lease_id = %s", (lease_id,))
        
        # 4. STATUS FLIP: Mark apartment as available again
        cursor.execute("UPDATE apartment SET is_available = 1 WHERE apartment_id = %s", (apartment_id,))
        
        db.commit()
        return penalty # Return the penalty so the UI can show it in a message box
        
    except Exception as e:
        print(f"Termination Error: {e}")
        return None
    finally:
        db.close()