import mqtt
import json

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    print("Incoming:", data)