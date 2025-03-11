from kafka import KafkaProducer
import uuid
from datetime import datetime
import random
import time
import json

# Kafka Configuration
KAFKA_BROKER = 'localhost:9092'
KAFKA_TOPIC = 'sensor-data'

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_data_point():
    """Generate a random data point with UUID, timestamp, and value"""
    return {
        "id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "value": round(random.uniform(0, 1000), 2)
    }

def produce_to_kafka(interval_ms=300):
    """Produce messages to Kafka at specified intervals"""
    try:
        while True:
            # Generate data
            data = generate_data_point()
            
            # Send to Kafka
            try:
                producer.send(KAFKA_TOPIC, value=data)
                print(f"Sent: {data}", flush=True)
            except Exception as e:
                print(f"Failed to send message: {str(e)}")
            
            # Wait for specified interval
            time.sleep(interval_ms / 1000)
            
    except KeyboardInterrupt:
        print("\nStopping data production...")
    finally:
        producer.close()

if __name__ == "__main__":
    print(f"Starting Kafka producer to {KAFKA_BROKER} on topic '{KAFKA_TOPIC}'")
    print("Press Ctrl+C to stop...")
    produce_to_kafka()
