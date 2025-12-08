"""
Script to test Supabase connection and create table if needed
"""
import psycopg2

# Supabase credentials
host = "db.qsqlawrciwrtrlotodke.supabase.co"
port = "5432"
database = "postgres"
user = "postgres"
password = "Ratan@181998"

print("🔗 Connecting to Supabase...")

try:
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    print("✅ Connected to Supabase successfully!")
    
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'telecom_data'
        );
    """)
    table_exists = cursor.fetchone()[0]
    
    if not table_exists:
        print("📝 Creating telecom_data table...")
        cursor.execute("""
            CREATE TABLE telecom_data (
                id SERIAL PRIMARY KEY,
                caller_name VARCHAR(256),
                receiver_name VARCHAR(256),
                caller_id VARCHAR(20),
                receiver_id VARCHAR(20),
                start_datetime TIMESTAMP,
                end_datetime TIMESTAMP,
                call_duration INTEGER,
                network_provider VARCHAR(50),
                total_amount DECIMAL(5,2)
            );
        """)
        conn.commit()
        print("✅ Table created successfully!")
    else:
        print("✅ Table 'telecom_data' already exists!")
    
    # Check row count
    cursor.execute("SELECT COUNT(*) FROM telecom_data")
    count = cursor.fetchone()[0]
    print(f"📊 Current row count: {count}")
    
    cursor.close()
    conn.close()
    print("✅ Connection closed.")
    
except Exception as e:
    print(f"❌ Error: {e}")
