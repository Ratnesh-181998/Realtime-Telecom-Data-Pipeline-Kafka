"""
Batch processor that reads messages from Kafka and writes to Postgres.
This version works reliably on Windows without streaming checkpoint issues.
"""
from kafka import KafkaConsumer
import psycopg2
import json
import time

print("🚀 Kafka to Postgres Batch Processor")
print("=" * 50)

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']
KAFKA_TOPIC = 'telecom-data'

# Postgres Configuration  
PG_HOST = 'localhost'
PG_PORT = '5438'
PG_DB = 'telecom_db'
PG_USER = 'admin'
PG_PASSWORD = 'password'

def get_postgres_connection():
    """Create a Postgres connection."""
    return psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )

def insert_record(conn, record):
    """Insert a single record into Postgres."""
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
        float(record['total_amount'])
    )
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()

def main():
    print(f"📡 Connecting to Kafka at {KAFKA_BOOTSTRAP_SERVERS}...")
    
    # Create Kafka consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='latest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')),
        consumer_timeout_ms=5000  # 5 second timeout for polling
    )
    
    print(f"✅ Connected to Kafka topic: {KAFKA_TOPIC}")
    print(f"🔗 Connecting to Postgres at {PG_HOST}:{PG_PORT}...")
    
    conn = get_postgres_connection()
    print("✅ Connected to Postgres!")
    print("\n🎧 Listening for messages... (Ctrl+C to stop)")
    print("-" * 50)
    
    record_count = 0
    
    try:
        while True:
            # Poll for messages
            messages = consumer.poll(timeout_ms=1000)
            
            for topic_partition, records in messages.items():
                for record in records:
                    data = record.value
                    
                    # Filter: only process positive call durations
                    if data.get('call_duration', 0) > 0:
                        insert_record(conn, data)
                        record_count += 1
                        print(f"📝 [{record_count}] Saved: {data['caller_name']} -> {data['receiver_name']} ({data['call_duration']}s)")
            
            # Small pause to prevent CPU spin
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print(f"\n\n⏹ Stopping...")
        print(f"📊 Total records saved: {record_count}")
    finally:
        consumer.close()
        conn.close()
        print("✅ Connections closed.")

if __name__ == "__main__":
    main()
