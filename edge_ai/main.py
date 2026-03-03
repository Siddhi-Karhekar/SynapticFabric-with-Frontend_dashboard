from simulator import stream
from processor import clean
from mqtt_publisher import publish

for data in stream():
    data = clean(data)
    if data:
        publish(data)