from flask import (
   flash, 
   redirect, 
   render_template, 
   request, 
   url_for,
   Flask,
   render_template,
   session
)
from flask_socketio import SocketIO, emit
import os
from sys import stderr
from datetime import datetime

from adapter.DbAdapter import DbAdapter
from model.SensorModel import SensorModel

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["DEBUG"] = True
app.config["PORT"] = 5000
DIR_FILE = os.path.join(os.path.dirname(__file__))
socketio = SocketIO(app)


@app.route("/")
def index():
   lpath = os.path.join(DIR_FILE, "file", "0.txt")
   ReferenceDbAdapter = DbAdapter(lpath)
   datos = ReferenceDbAdapter.get()
   user = {
            "id": "0",
            "name": "administrator",
            "is_authenticated": True,
   }
   # VALUES IN FORMAT
   # "id","write_at","value"
   timestamp = list()
   temperature = list()
   for idx, item in enumerate(datos):
      timestamp.append(idx)
      temperature.append(float(item[2]))
   return render_template("index.html", title="index", temperature=temperature, timestamp=timestamp, current_user=user)

@socketio.on("connect")
def on_connect():
   """
   This function will set the file that contains the sensor data
   """
   # params = ["id", "write_at_str", "value"]
   # data = request.json()
   # for item in params:
   #    if dat0a.get(item) is None:
   #       raise KeyError(f"Invalid key {item}")
   # json_data["sensorid"] = json_data.pop["id"]
   # json_data["write_at"] = datetime.strptime(json_data.pop["write_at_str"], "%d/%m/%y %H:%M:%S")
   # ReferenceSensor = SensorModel(json_data)
   # lpath = os.path.join(DIR_FILE, "file", json_data["sensorid"] + ".json")
   # ReferenceDbAdapter = DbAdapter(lpath)
   # ReferenceDbAdapter.save(ReferenceSensor.to_json())
   # emit("new_message", ReferenceSensor.to_dict(), broadcast=True)
   lpath = os.path.join(DIR_FILE, "file", "0.txt")
   ReferenceDbAdapter = DbAdapter(lpath)
   emit("temperature", (len(ReferenceDbAdapter.get())+1, 40))


if __name__ == "__main__":
   socketio.run(app)