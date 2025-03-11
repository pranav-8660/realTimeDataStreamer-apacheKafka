from kafka import KafkaProducer
import json
import requests
import time

API_KEY_VINTAGE = "WACL3P7R4H6DJFSG"
STOCK_SYMBOL="AAPL"
KAFKA_TOPIC="stock-prices"
KAFKA_BROKER="localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v:json.dumps(v).encode("utf-8")
)

def fetch_stock_price():
    
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK_SYMBOL}&interval=1min&apikey={API_KEY_VINTAGE}"
    response = requests.get(url)
    data = response.json()
    if "Time Series (1min)" in data:
        latest_timestamp = list(data["Time Series (1min)"].keys())[0]
        stock_info = data["Time Series (1min)"][latest_timestamp]
        stock_data = {
            "timestamp":latest_timestamp,
            "symbol":STOCK_SYMBOL,
            "open":float(stock_info["1. open"]),
            "high":float(stock_info["2. high"]),
            "low":float(stock_info["3. low"]),
            "close":float(stock_info["4. close"]),
            "volume":float(stock_info["5. volume"])
        
        }
        return stock_data
    return None

if __name__ == "__main__":
    while True:
        stock_data = fetch_stock_price()
        if stock_data:
            print(f"Stock data is fetched, sendind to kafka-broker this data-> {stock_data}")
            producer.send(KAFKA_TOPIC,value=stock_data)
        time.sleep(60)