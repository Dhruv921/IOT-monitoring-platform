from sqlite3 import connect

import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime, timezone

MQTT_HOST = "localhost"
MQTT_PORT = 1883
CYCLIC_SECONDS = 3


class Sensor:
    def __init__(self, sensor_id, room, base_temp, base_hum): 
        self.sensor_id = sensor_id
        self.temperature = base_temp
        self.humidity = base_hum
        self.topic = f"building/{room}/{sensor_id}/telemetry"
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=self.sensor_id)
        
    def connect(self):
        self.client.connect(MQTT_HOST, MQTT_PORT)
        self.client.loop_start()

    def publish_once(self):
        #random walk: small step from the previous value
        self.temperature += random.uniform(-0.3, 0.3)
        self.humidity += random.uniform(-0.5, 0.5)
        #keep values in realistic range
        self.temperature = max(15, min(30, self.temperature))
        self.humidity = max(20, min(80, self.humidity))
        data={
            "sensor_id": self.sensor_id,
            "temperature": round(self.temperature, 2),
            "humidity": round(self.humidity, 2),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        payload = json.dumps(data)
        self.client.publish(self.topic,payload, qos=1)
        print(f"{self.topic} -> {payload}")

sensors = [
    Sensor("sensor-01", "room1", 24.0, 40.0),
    Sensor("sensor-02", "room2", 25.0, 45.0),
    Sensor("sensor-03", "room3", 23.5, 42.0),
    Sensor("sensor-04", "room1", 24.5, 41.0),
    Sensor("sensor-05", "room2", 25.5, 43.0)
]

for sensor in sensors:
        sensor.connect()
try:
    while True:
        for sensor in sensors:
            sensor.publish_once()
            time.sleep(random.uniform(0.1, 0.5))
        time.sleep(CYCLIC_SECONDS)
except KeyboardInterrupt:
    print("Exiting...")
