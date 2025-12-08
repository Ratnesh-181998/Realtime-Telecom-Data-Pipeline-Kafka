from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType, IntegerType
import os
import sys

# Set Hadoop home for Windows
os.environ['HADOOP_HOME'] = r'C:\hadoop'
os.environ['PATH'] = os.environ.get('PATH', '') + r';C:\hadoop\bin'

# Package dependencies
kafka_package = "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0"
postgres_package = "org.postgresql:postgresql:42.6.0"

print("🔧 Initializing Spark Session...")

try:
    spark = SparkSession.builder \
        .appName("PySpark Kafka to Postgres Stream") \
        .master("local[*]") \
        .config("spark.jars.packages", f"{kafka_package},{postgres_package}") \
        .config("spark.driver.memory", "2g") \
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    print("✅ Spark Session Created!")

    # Kafka Configuration
    kafka_bootstrap_servers = 'localhost:9092'
    kafka_topic = 'telecom-data'

    # Schema
    schema = StructType() \
        .add("caller_name", StringType()) \
        .add("receiver_name", StringType()) \
        .add("caller_id", StringType()) \
        .add("receiver_id", StringType()) \
        .add("start_datetime", StringType()) \
        .add("end_datetime", StringType()) \
        .add("call_duration", IntegerType()) \
        .add("network_provider", StringType()) \
        .add("total_amount", StringType())

    print(f"📡 Connecting to Kafka at {kafka_bootstrap_servers}...")

    # Read from Kafka
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
        .option("subscribe", kafka_topic) \
        .option("startingOffsets", "latest") \
        .option("failOnDataLoss", "false") \
        .load()

    # Parse JSON
    parsed_df = df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    # Filter valid records
    filtered_df = parsed_df.filter(col("call_duration") > 0)

    # Postgres Config
    postgres_url = "jdbc:postgresql://localhost:5438/telecom_db"
    postgres_props = {
        "user": "admin",
        "password": "password",
        "driver": "org.postgresql.Driver"
    }

    def write_batch(batch_df, batch_id):
        count = batch_df.count()
        if count > 0:
            print(f"\n📊 Batch {batch_id}: {count} records")
            batch_df.show(5, truncate=False)
            
            # Write to Postgres
            batch_df.write \
                .jdbc(url=postgres_url, table="telecom_data", mode="append", properties=postgres_props)
            print(f"✅ Batch {batch_id} saved to Postgres!")
        else:
            print(f"⏳ Batch {batch_id}: waiting for data...")

    print("\n🚀 Starting stream...")
    print("=" * 60)

    # Create checkpoint directory
    checkpoint_path = r"C:\tmp\spark-checkpoint\telecom2"
    os.makedirs(checkpoint_path, exist_ok=True)

    query = filtered_df.writeStream \
        .foreachBatch(write_batch) \
        .outputMode("update") \
        .option("checkpointLocation", checkpoint_path) \
        .trigger(processingTime="5 seconds") \
        .start()

    query.awaitTermination()

except KeyboardInterrupt:
    print("\n⏹ Stopping...")
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
finally:
    if 'spark' in dir():
        spark.stop()
