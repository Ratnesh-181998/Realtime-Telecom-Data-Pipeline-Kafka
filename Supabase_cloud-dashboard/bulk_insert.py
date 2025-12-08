"""
Bulk insert 500 records into Supabase for demo purposes
"""
import psycopg2
from faker import Faker
import random
from datetime import datetime, timedelta

# Supabase credentials
SUPABASE_HOST = "db.qsqlawrciwrtrlotodke.supabase.co"
SUPABASE_PORT = "5432"
SUPABASE_DB = "postgres"
SUPABASE_USER = "postgres"
SUPABASE_PASSWORD = "Ratan@181998"

fake = Faker()
PROVIDERS = ['Verizon', 'AT&T', 'T-Mobile', 'Sprint']

def generate_records(n=500):
    """Generate n fake call records."""
    records = []
    base_time = datetime.now() - timedelta(hours=24)
    
    for i in range(n):
        call_duration = random.randint(30, 1200)
        start_time = base_time + timedelta(minutes=i * 2.88 + random.randint(0, 10))  # Spread over 24 hours
        end_time = start_time + timedelta(seconds=call_duration)
        
        records.append((
            fake.name(),
            fake.name(),
            f'+1{fake.numerify("##########")}',
            f'+1{fake.numerify("##########")}',
            start_time,
            end_time,
            call_duration,
            random.choice(PROVIDERS),
            round((call_duration / 60) * 0.05, 2)
        ))
    return records

def main():
    print("🚀 Bulk Insert to Supabase")
    print("=" * 50)
    
    conn = psycopg2.connect(
        host=SUPABASE_HOST,
        port=SUPABASE_PORT,
        database=SUPABASE_DB,
        user=SUPABASE_USER,
        password=SUPABASE_PASSWORD
    )
    print("✅ Connected!")
    
    print("📝 Generating 500 records...")
    records = generate_records(500)
    
    print("⏳ Inserting records...")
    cursor = conn.cursor()
    
    sql = """
        INSERT INTO telecom_data 
        (caller_name, receiver_name, caller_id, receiver_id, 
         start_datetime, end_datetime, call_duration, network_provider, total_amount)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.executemany(sql, records)
    conn.commit()
    
    print(f"✅ Inserted {len(records)} records!")
    
    cursor.execute("SELECT COUNT(*) FROM telecom_data")
    total = cursor.fetchone()[0]
    print(f"📊 Total records in database: {total}")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
