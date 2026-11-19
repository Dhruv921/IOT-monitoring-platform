from sqlite3 import connect

import paho.mqtt.client as mqtt
import json
import os





MQTT_HOST = os.getenv("MQTT_HOST", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="ingestor")

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected with result code {reason_code}")
    client.subscribe("building/+/+/telemetry", qos=1)

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"Received message on topic {msg.topic}: {payload}")
    try:
        json_payload = json.loads(payload)
    except json.JSONDecodeError:
        print("Failed to decode JSON payload")
        return
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_HOST, MQTT_PORT)
client.loop_forever()



# class Sensor:
#     def __init__(self, sensor_id, room, base_temp, base_hum,):
#         self.sensor_id = sensor_id
#         self.temperature = base_temp
#         self.humidity = base_hum
#         self.status_topic = f"building/{room}/{sensor_id}/status"
#         self.topic = f"building/{room}/{sensor_id}/telemetry"
#         self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=self.sensor_id)
        
#     def connect(self):
#         self.client.will_set(self.status_topic, payload="offline", qos=1, retain=True)
#         self.client.connect(MQTT_HOST, MQTT_PORT, keepalive=10)
#         self.client.loop_start()
#         self.client.publish(self.status_topic, "online", qos=1, retain=True)


#     def publish_once(self):
#         #random walk: small step from the previous value
#         self.temperature += random.uniform(-0.3, 0.3)
#         self.humidity += random.uniform(-0.5, 0.5)
#         #keep values in realistic range
        
#         self.temperature = max(15, min(30, self.temperature))
#         temp_to_send = self.temperature
#         if random.random() < 0.02:  # 5% chance to send an outlier temperature
#             temp_to_send += random.uniform(35,40)
#         self.humidity = max(20, min(80, self.humidity))
#         data={
#             "sensor_id": self.sensor_id,
#             "temperature": round(self.temperature, 2),
#             "humidity": round(self.humidity, 2),
#             "timestamp": datetime.now(timezone.utc).isoformat(),
#             "temp_to_send": round(temp_to_send, 2)
#         }
#         payload = json.dumps(data)
#         self.client.publish(self.topic,payload, qos=1)
#         print(f"{self.topic} -> {payload}")

# sensors = [
#     Sensor("sensor-01", "room1", 24.0, 40.0),
#     Sensor("sensor-02", "room2", 25.0, 45.0),
#     Sensor("sensor-03", "room3", 23.5, 42.0),
#     Sensor("sensor-04", "room4", 24.5, 41.0),
#     Sensor("sensor-05", "room5", 25.5, 43.0)
# ]

# for sensor in sensors:
#         sensor.connect()
# try:
#     while True:
#         for sensor in sensors:
#             sensor.publish_once()
#             time.sleep(random.uniform(0.1, 0.5))
#         time.sleep(CYCLIC_SECONDS)
# except KeyboardInterrupt:
#     for sensor in sensors:
#         sensor.client.loop_stop()
#         sensor.client.disconnect()
    
#     print("Exiting...")

