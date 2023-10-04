import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
from datetime import datetime
import json

MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

def on_connect(client, userdata, flag, rc):
	print("Connected")
def on_publish(client, userdata, mid):
	print("published")
	
#mqtt client setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_publish = on_publish

print("Connwection result: ", client.connect(MQTT_BROKER, MQTT_PORT,60))

client.loop_start()

RELAY_PIN = 23
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11,4)
    if humidity is not None:
        currenttime=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"Date/Time:{currenttime}")
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%")
        if 70.0 > humidity > 60.0:
            GPIO.output(RELAY_PIN, GPIO.HIGH)  
            print("Relay is ON")
        else:
            GPIO.output(RELAY_PIN, GPIO.LOW)  
            print("Relay is OFF")

        payload = {
        "temperature" : temperature,
        "humidity" : humidity,
        "currenttime" : time.strftime("%Y-%m-%d %H:%M:%S") 

         }
        print(payload)
        
        client.publish("payload", json.dumps(payload))

    else:
        print("Failed to retrieve temperature data from sensor")
    time.sleep(5)