import mysql.connector
from datetime import datetime, timedelta

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="pams_db"
    )

# 1. Create a New Lease
def create_lease(tenant_ni, apartment_id, start_date, duration_months):
    db = get_db_connection()
    cursor = db.cursor()
    
    # Calculate end date
    start_dt = datetime.strptime(start_date, '%Y-%m-%d')
    end_dt = start_dt + timedelta(days=duration_months * 30)
    
    try:
        # Insert the Lease
        query = """INSERT INTO leases (tenant_ni, apartment_id, start_date, end_date, status) 
                   VALUES (%s, %s, %s, %s, 'Active')"""
        cursor.execute(query, (tenant_ni, apartment_id, start_date, end_dt.date()))
        
        # IMPORTANT: Update Apartment status to 'Occupied'
        cursor.execute("UPDATE apartments SET status = 'Occupied' WHERE id = %s", (apartment_id,))
        
        db.commit()
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        db.close()

# 2. Early Termination Logic (The Penalty)
def process_early_termination(lease_id, monthly_rent):
    """
    Rule: 5% penalty of monthly rent.
    Note: Front-end handles the 1-month notice check.
    """
    penalty_amount = float(monthly_rent) * 0.05
    
    db = get_db_connection()
    cursor = db.cursor()
    
    try:
        # 1. Update Lease Status
        cursor.execute("UPDATE leases SET status = 'Terminated' WHERE id = %s", (lease_id,))
        
        # 2. Get Apartment ID from this lease to make it 'Available' again
        cursor.execute("SELECT apartment_id FROM leases WHERE id = %s", (lease_id,))
        apt_id = cursor.fetchone()[0]
        cursor.execute("UPDATE apartments SET status = 'Available' WHERE id = %s", (apt_id,))
        
        # 3. (Optional) Insert penalty into a 'payments' or 'billing' table for Finance Manager
        # cursor.execute("INSERT INTO bills (lease_id, amount, type) VALUES (%s, %s, 'Termination Penalty')", (lease_id, penalty_amount))
        
        db.commit()
        return penalty_amount
    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        db.close()