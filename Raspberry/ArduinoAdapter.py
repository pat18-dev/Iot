import serial
from socketIO_client import SocketIO, BaseNamespace
from datetime import datetime

import random

class Namespace(BaseNamespace):

   def on_connect(self):
      print('[Connected]')

   def on_reconnect(self):
      print('[Reconnected]')

   def on_disconnect(self):
      print('[Disconnected]')
      
def send_to_server(URL: str):
   with SocketIO(URL, 5000, Namespace) as socketIO:
      ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
      ser.reset_input_buffer()
      line = ser.readline().decode("utf-8").rstrip()
      data = {"id": 1, "write_at_str": datetime.now().strftime("%d/%m/%y %H:%M:%S"), "value": float(line)}
      socketIO.emit("send_data", data)
      
def send_to_server(URL, data):
   for i in range(1,max_idx):
      with SocketIO(URL, 5000, Namespace) as socketIO:
         line = random.randint(5, 15)
         data = {"id": 1, "write_at_str": datetime.now().strftime("%d/%m/%y %H:%M:%S"), "value": float(line)}
         socketIO.emit("send_data", data)

def get_data():
   ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
   ser.reset_input_buffer()
   line = ser.readline().decode("utf-8").rstrip()
   return line
   
if __name__ == "__main__":
   URL = "http://192.168.0.34"
   data = float(get_data())
   test_send_to_server(URL,10)
   # send_to_server(URL)