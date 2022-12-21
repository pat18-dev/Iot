import requests
from datetime import datetime

if __name__ == "__main__":
    data = {"id": "1", "time": datetime.now().strftime("%d/%m/%y %H:%M:%S"), "value": "20.54"}
    URL = "http://127.0.0.1:5000/new_message/"
    response = requests.post(URL, data=data)
    print(response.text)
