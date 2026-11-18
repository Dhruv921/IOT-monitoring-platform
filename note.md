Broker: the servetr that receives all msg and forwards them.
Publisher:a client that sends a messages(your sensor)
Subscriber:a client that recives messages (your ingestor)
Topic:the address of the message, like building/room1/sensor-01/telemetry. The / saparates levels.
Wildcards: + matches one level(building/+/sensor-01/telemetry), and # mtches everything below (building/#).
Qos:delivery guarantee. 0 is at most once. 1 is at least once, 2 is exactly once.
Retained message: the broker stores the last message on the toic and gives it to every new subscriber immedietly.  
The last will (a message the broker sends if a client disconnects unexpectedly) we use in Block 3.
