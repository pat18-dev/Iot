import serial
import requests
from datetime import datetime

textfile = open('ArduinoData.txt','w')


URL = 'http://localhost:5000/send/'

if __name__ == '__main__':
   ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
   ser.reset_input_buffer()
   
   while True:
      print(b"Initialization starts!\n")
      if ser.in_waiting > 0:
         line = ser.readline().decode('utf-8').rstrip()
         now = datetime.now().strftime("%H:%M")
         #data = {"data": line, "time": now}
         #response = requests.post(URL, data = data)
         
   textfile.write(line)

   #print(response.text)