import serial
import json
import time
import requests

data = {}

print("Start")
port = "COM4"
bluetooth = serial.Serial(port, 9600)
print("Connected")
bluetooth.flushInput()

while True:
    print("Ping")
    input_data = bluetooth.readline()
    data = json.loads(input_data.decode())

    print(data)

    requests.post("http://192.168.1.244:8000/movement", json=data)

    time.sleep(0.5)

bluetooth.close()
print("Done")
