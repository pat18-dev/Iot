import random

import logging
from socketIO_client import SocketIO, LoggingNamespace, BaseNamespace

from datetime import datetime

class Namespace(BaseNamespace):

    def on_connect(self):
        print('[Connected]')

    def on_reconnect(self):
        print('[Reconnected]')

    def on_disconnect(self):
        print('[Disconnected]')

if __name__ == "__main__":
    URL = "http://127.0.0.1:5000/send_data"
    with SocketIO('localhost', 5000, Namespace) as socketIO:
        for i in range(0, 10):
            data = {"id": 1, "write_at_str": datetime.now().strftime("%d/%m/%y %H:%M:%S"), "value": random.uniform(100, 200)}
            socketIO.emit("send_data", data)
            socketIO.wait(seconds=2)