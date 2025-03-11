# Real-Time Data Pipeline with Kafka and PostgreSQL

A production-grade data pipeline demonstrating real-time data generation, streaming via Kafka, and storage in PostgreSQL.

## 📥 Prerequisites
- Python 3.8+
- Apache Kafka 3.0+
- PostgreSQL 14+
- Java 11+ (for Kafka)
- libpq-dev (PostgreSQL dev files)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install kafka-python psycopg2-binary python-dotenv uuid

# Start Zookeeper
$KAFKA_HOME/bin/zookeeper-server-start.sh $KAFKA_HOME/config/zookeeper.properties

# Start Kafka Server (new terminal)
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties

# Create Topic
$KAFKA_HOME/bin/kafka-topics.sh --create \
  --topic sensor-data \
  --bootstrap-server localhost:9092 \
  --partitions 1 \
  --replication-factor 1

CREATE DATABASE sensor_data;
\c sensor_data

CREATE TABLE sensor_readings (
    id UUID PRIMARY KEY,
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    value NUMERIC(10,2) NOT NULL
);

CREATE USER pipeline_user WITH PASSWORD 'SecurePass123!';
GRANT CONNECT, TEMPORARY ON DATABASE sensor_data TO pipeline_user;
GRANT USAGE ON SCHEMA public TO pipeline_user;
GRANT INSERT, SELECT ON ALL TABLES IN SCHEMA public TO pipeline_user;

# Kafka
KAFKA_BROKER=localhost:9092
KAFKA_TOPIC=sensor-data

# PostgreSQL
PG_HOST=localhost
PG_DB=sensor_data
PG_USER=pipeline_user
PG_PASSWORD=SecurePass123!
PG_PORT=5432

python producer.py

{
  "id": "a1b2c3d4...", 
  "timestamp": "2023-10-05T12:34:56.789", 
  "value": 123.45
}

python consumer.py

$KAFKA_HOME/bin/kafka-console-consumer.sh \
  --bootstrap-server localhost:9092 \
  --topic sensor-data \
  --from-beginning

-- Check latest 5 records
SELECT * FROM sensor_readings ORDER BY timestamp DESC LIMIT 5;

-- Verify counts
SELECT COUNT(*) FROM sensor_readings;
