# Real-Time Telecom Data Pipeline 🚀

A comprehensive real-time streaming project that generates synthetic telecom data, streams it through **Apache Kafka**, and stores it in a **PostgreSQL** data warehouse (simulating Amazon Redshift for local development).

![Pipeline Architecture](Screenshot%202024-04-16%20at%2016.16.20.png)

## 🏗 Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Data Source   │────▶│  Apache Kafka   │────▶│   PostgreSQL    │
│ (Python Producer)│     │  (Docker)       │     │   (Docker)      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
   Generates               Message                  Data
   Fake CDRs               Broker                 Warehouse
```

1. **Data Source**: Python Producer generating fake Call Data Records (CDRs)
2. **Message Broker**: Apache Kafka (running in Docker)
3. **Stream Processing**: Python/PySpark consumer processing messages
4. **Storage**: PostgreSQL Database (Local Docker container - simulates Redshift)

## 🛠 Prerequisites

- **Docker Desktop** (Required for Kafka, Zookeeper & Postgres)
- **Python 3.8+**
- **Java 11 or 17** (Required for Spark)

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/kafka-spark-redshift-streaming.git
cd kafka-spark-redshift-streaming
```

### 2. Install Python Dependencies
```bash
pip install kafka-python-ng pyspark faker psycopg2-binary
```

### 3. Start Infrastructure
Start Kafka, Zookeeper, and PostgreSQL using Docker Compose:
```bash
docker-compose up -d
```

Wait ~60 seconds for all services to become healthy.

### 4. Initialize Database
Create the `telecom_data` table in PostgreSQL:
```bash
# PowerShell (Windows)
Get-Content postgres_create_table.sql | docker exec -i postgres psql -U admin -d telecom_db

# Bash (Linux/Mac)
docker exec -i postgres psql -U admin -d telecom_db < postgres_create_table.sql
```

## ▶️ How to Run

### Option 1: Simple Python Consumer (Recommended)
```bash
# Terminal 1: Start the Data Producer
python kafka_producer.py

# Terminal 2: Start the Consumer
python kafka_to_postgres.py
```

### Option 2: PySpark Streaming (Advanced)
```bash
# Terminal 1: Start the Data Producer
python kafka_producer.py

# Terminal 2: Start Spark Streaming
python spark_redshift_stream.py
```

### 3. Verify Data
Check if data is landing in the database:
```bash
python postgres_connect.py
```

Or query directly:
```bash
docker exec -it postgres psql -U admin -d telecom_db -c "SELECT * FROM telecom_data LIMIT 5;"
```

## 📂 Project Structure

| File | Description |
|------|-------------|
| `docker-compose.yml` | Infrastructure as Code (Kafka, Zookeeper, Postgres) |
| `kafka_producer.py` | Python script to generate and push mock telecom data |
| `kafka_to_postgres.py` | Simple Python consumer - reads Kafka, writes to Postgres |
| `spark_redshift_stream.py` | PySpark Streaming implementation |
| `postgres_create_table.sql` | SQL DDL for the destination table |
| `postgres_connect.py` | Utility to test database connection |
| `redshift-jdbc42-2.1.0.12.jar` | JDBC Driver for Redshift connectivity |

## 🔧 Configuration

### Ports Used
| Service | Port |
|---------|------|
| Kafka | 9092 |
| Zookeeper | 2181 |
| PostgreSQL | 5438 |
| Spark Master UI | 9090 |
| Kafka Control Center | 9021 |
| Schema Registry | 8081 |

### Sample Data Generated
```json
{
  "caller_name": "John Smith",
  "receiver_name": "Jane Doe",
  "caller_id": "+11234567890",
  "receiver_id": "+10987654321",
  "start_datetime": "2024-01-15 10:30:00",
  "end_datetime": "2024-01-15 10:45:00",
  "call_duration": 900,
  "network_provider": "Verizon",
  "total_amount": 0.75
}
```

## 📝 Notes

- This project uses a local PostgreSQL instance to simulate Amazon Redshift for cost-free development
- To switch to AWS Redshift, update the JDBC URL in `spark_redshift_stream.py` and use the Redshift driver
- The `kafka_to_postgres.py` script is recommended for Windows users due to Spark streaming checkpoint issues

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

---
**Created by Ratnesh Singh** | Data Engineer Portfolio Project
