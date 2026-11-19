import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime, timezone

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="sensor-01")
client.connect("localhost", 1883)
client.loop_start()
try:
    while True:
        dict = {"sensor_id": "sensor-01", "temperature": 24.00 + random.uniform(-0.3, 0.3), "humidity": 40 + random.uniform(-0.3,0.3), "timestamp": datetime.now(timezone.utc).isoformat()}
        json.dumps(dict)
        client.publish(topic = "building/room1/sensor-01/telemetry", payload =str(dict) , qos = 1)
        datetime.now(timezone.utc).isoformat()
        time.sleep(3)

except KeyboardInterrupt:
    print("Exiting...")
    