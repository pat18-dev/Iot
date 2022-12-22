import serial
import requests
from datetime import datetime

URL = "http://190.119.114.196:5000/send_data/"

if __name__ == "__main__":
   ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
   ser.reset_input_buffer()

   while True:
      print(b"Initialization starts!\n")
      if ser.in_waiting > 0:
         line = ser.readline().decode("utf-8").rstrip()
         now = datetime.now().strftime("%d/%m/%y %H:%M:%S")
         data = [1, now, line]
         response = requests.post(URL, data=data)
         print(response.text)
