import serial
from socketIO_client import SocketIO, BaseNamespace
from datetime import datetime

class Namespace(BaseNamespace):

   def on_connect(self):
      print('[Connected]')

   def on_reconnect(self):
      print('[Reconnected]')

   def on_disconnect(self):
      print('[Disconnected]')


if __name__ == "__main__":
   URL = "http://190.119.114.196:5000/send_data/"
   ser = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
   ser.reset_input_buffer()
   with SocketIO('localhost', 5000, Namespace) as socketIO:
      for i in range(0, 10):
         line = ser.readline().decode("utf-8").rstrip()
         data = {"id": 1, "write_at_str": datetime.now().strftime("%d/%m/%y %H:%M:%S"), "value": float(line)}
         socketIO.emit("send_data", data)
         # socketIO.wait(seconds=2)
