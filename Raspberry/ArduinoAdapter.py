import serial
import requests
from socketIO_client import SocketIO, BaseNamespace
from datetime import datetime

import random

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
URL = "http://192.168.0.34"
PORT = "5000"

def send_post():
   ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
   ser.reset_input_buffer()
   line = ser.readline().decode("utf-8").rstrip()
   data = {"id": 1, "write_at_str": datetime.now().strftime(DATE_FORMAT), "value": float(line)}
   x = requests.post(URL + ":" + PORT, json = data)
   print("---RESPONSE")
   print(x)
   
def test_send_post():
   line = random.randint(5,15)
   data = {"id": 1, "write_at_str": datetime.now().strftime(DATE_FORMAT), "value": float(line)}
   x = requests.post(URL + ":" + PORT, json = data)
   print("---RESPONSE")
   print(x)
   
if __name__ == "__main__":
   test_send_post()
   # send_post()