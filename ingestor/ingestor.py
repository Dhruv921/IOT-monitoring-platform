
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
from datetime import datetime


import paho.mqtt.client as mqtt
import json
import os
from pathlib import Path
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

# Mqtt configuration
MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))


INFLUX_URL = os.getenv("INFLUX_URL", "http://localhost:8086")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG", "IOTt-Lab")
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET", "Sensors")

REQUIRED_KEYS = ["temperature", "humidity", "sensor_id", "timestamp"]
# Load environment variables from .env file & initialize InfluxDB client

influx = InfluxDBClient(url=INFLUX_URL, token=INFLUX_TOKEN, org=INFLUX_ORG)
write_api = influx.write_api(write_options=SYNCHRONOUS)







client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="ingestor")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("building/+/+/telemetry", qos=1)



def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    
    
    try:
        json_payload = json.loads(payload)
    except (json.JSONDecodeError, UnicodeDecodeError):
        print("Failed to decode JSON payload ")
        return


    if not isinstance(json_payload, dict):
        print(f"WARNING: payload is not an object on {msg.topic}")
        return
    for key in REQUIRED_KEYS:
        if key not in payload:
            print(f"WARNING: missing key '{key}' on {msg.topic}")
            return

        # c) build the InfluxDB point and write it
    try:
        room = msg.topic.split("/")[1]
        point =(
            Point("environment")
            .tag("sensor_id", json_payload["sensor_id"])
            .tag("room", room)
            .field("temperature", float(json_payload["temperature"]))
            .field("humidity", float(json_payload["humidity"]))
            .time(datetime.fromisoformat(json_payload["timestamp"]))
        )
        write_api.write(bucket=INFLUX_BUCKET, record=point)
        print(f"OK {json_payload['sensor_id']} {json_payload['temperature']} ")
    except Exception as e:
        print(f"Failed to write point to InfluxDB: {e}")
        
    
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_HOST, MQTT_PORT)
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("Ingestor stopped")
    client.disconnect()
    influx.close()
