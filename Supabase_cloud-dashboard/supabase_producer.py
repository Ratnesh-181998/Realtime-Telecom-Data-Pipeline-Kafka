"""
Supabase Data Producer
Generates fake telecom data and inserts directly into Supabase
This can run anywhere - locally or in the cloud!
"""
import psycopg2
from faker import Faker
import random
import time
from datetime import datetime, timedelta

# Supabase credentials
SUPABASE_HOST = "db.qsqlawrciwrtrlotodke.supabase.co"
SUPABASE_PORT = "5432"
SUPABASE_DB = "postgres"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "Ratan@181998"

# Initialize Faker
fake = Faker()

# Network providers
PROVIDERS = ['Verizon', 'AT&T', 'T-Mobile', 'Sprint']

def get_connection():
    """Create database connection."""
    return psycopg2.connect(
        host=SUPABASE_HOST,
        port=SUPABASE_PORT,
        database=SUPABASE_DB,
        user=SUPABASE_USER,
        password=SUPABASE_PASSWORD
    )

def generate_call_record():
    """Generate a single fake call record."""
    call_duration = random.randint(30, 1200)  # 30 seconds to 20 minutes
    start_time = datetime.now() - timedelta(minutes=random.randint(0, 60))
    end_time = start_time + timedelta(seconds=call_duration)
    
    return {
        'caller_name': fake.name(),
        'receiver_name': fake.name(),
        'caller_id': f'+1{fake.numerify("##########")}',
        'receiver_id': f'+1{fake.numerify("##########")}',
        'start_datetime': start_time,
        'end_datetime': end_time,
        'call_duration': call_duration,
        'network_provider': random.choice(PROVIDERS),
        'total_amount': round((call_duration / 60) * 0.05, 2)
    }

def insert_record(conn, record):
    """Insert a record into the database."""
    cursor = conn.cursor()
    sql = """
        INSERT INTO telecom_data 
        (caller_name, receiver_name, caller_id, receiver_id, 
         start_datetime, end_datetime, call_duration, network_provider, total_amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        record['caller_name'],
        record['receiver_name'],
        record['caller_id'],
        record['receiver_id'],
        record['start_datetime'],
        record['end_datetime'],
        record['call_duration'],
        record['network_provider'],
        record['total_amount']
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()

def main():
    print("=" * 60)
    print("🚀 Supabase Data Producer")
    print("=" * 60)
    print(f"📡 Connecting to Supabase at {SUPABASE_HOST}...")
    
    try:
        conn = get_connection()
        print("✅ Connected to Supabase!")
        print("")
        print("📝 Generating and inserting records...")
        print("   Press Ctrl+C to stop")
        print("-" * 60)
        
        record_count = 0
        
        while True:
            # Generate and insert a record
            record = generate_call_record()
            insert_record(conn, record)
            record_count += 1
            
            # Print status
            print(f"📞 [{record_count}] {record['caller_name']} → {record['receiver_name']} "
                  f"({record['call_duration']}s, {record['network_provider']}, ${record['total_amount']})")
            
            # Wait 3 seconds before next record
            time.sleep(3)
            
    except KeyboardInterrupt:
        print(f"\n\n⏹ Stopping...")
        print(f"📊 Total records inserted: {record_count}")
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()
            print("✅ Connection closed.")

if __name__ == "__main__":
    main()
