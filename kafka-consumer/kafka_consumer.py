from kafka import KafkaConsumer
import psycopg2
import json
import os
from datetime import datetime

# Configuration
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'sensor-data'
POSTGRES_CONFIG = {
    'dbname': 'random_values',
    'user': 'pranav',
    'password': '12345',
    'host': 'localhost',
    'port': '5432'
}

def create_postgres_connection():
    """Create and return a PostgreSQL connection"""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error connecting to PostgreSQL: {e}")
        return None

def save_to_postgres(data, conn):
    """Save data to PostgreSQL database"""
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO sensor_readings (id, timestamp, value)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, (data['id'], data['timestamp'], data['value']))
        conn.commit()
    except (psycopg2.DatabaseError, psycopg2.InterfaceError) as e:
        print(f"Database error: {e}")
        conn.rollback()

def consume_from_kafka():
    """Consume messages from Kafka and store in PostgreSQL"""
    # Initialize Kafka Consumer
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    # Initialize PostgreSQL connection
    pg_conn = create_postgres_connection()
    if not pg_conn:
        return

    try:
        for message in consumer:
            data = message.value
            print(f"Received: {data}")
            
            # Convert ISO timestamp to PostgreSQL-compatible format
            try:
                data['timestamp'] = datetime.fromisoformat(data['timestamp'])
            except (KeyError, ValueError) as e:
                print(f"Invalid timestamp format: {e}")
                continue
                
            save_to_postgres(data, pg_conn)
            
    except KeyboardInterrupt:
        print("\nStopping consumer...")
    finally:
        consumer.close()
        if pg_conn:
            pg_conn.close()

if __name__ == "__main__":
    print("Starting Kafka Consumer with PostgreSQL storage...")
    consume_from_kafka()
