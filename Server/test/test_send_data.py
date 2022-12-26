import random

from socketIO_client import SocketIO, LoggingNamespace

from datetime import datetime

if __name__ == "__main__":
    URL = "http://127.0.0.1:5000/send_data"
    with SocketIO('localhost', 5000, LoggingNamespace) as socketIO:
        for i in range(0, 10):
            data = {"id": 1, "write_at_str": datetime.now().strftime("%d/%m/%y %H:%M:%S"), "value": random.uniform(100, 200)}
            socketIO.emit("send_data", data)