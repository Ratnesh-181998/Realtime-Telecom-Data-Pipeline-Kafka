import psycopg2

# Postgres connection parameters (Local Docker)
host = "localhost"
port = "5438"
dbname = "telecom_db"
user = "admin"
password = "password"

# Connection string
conn_string = f"dbname='{dbname}' user='{user}' host='{host}' port='{port}' password='{password}'"

# Connect to Postgres
try:
    print(f"Connecting to {host}:{port}/{dbname}...")
    conn = psycopg2.connect(conn_string)
    print("✅ Connected to Postgres successfully!")

    # Create a cursor
    cursor = conn.cursor()

    # Execute a query
    query = "SELECT version();"
    cursor.execute(query)

    # Fetch and print the result
    version = cursor.fetchone()
    print(f"📦 Database Version: {version[0]}")

    # Check if table exists
    cursor.execute("SELECT to_regclass('public.telecom_data');")
    table_exists = cursor.fetchone()[0]
    if table_exists:
        print("✅ Table 'telecom_data' exists.")
        
        # Check count
        cursor.execute("SELECT COUNT(*) FROM telecom_data;")
        count = cursor.fetchone()[0]
        print(f"📊 Current row count: {count}")
    else:
        print("⚠️ Table 'telecom_data' does NOT exist yet. Run the SQL script!")

    # Close the cursor and connection
    cursor.close()
    conn.close()

except Exception as error:
    print(f"❌ Error: {error}")
