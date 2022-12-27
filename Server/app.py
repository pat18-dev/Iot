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
from flask_socketio import SocketIO
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
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def index():
   # lpath = os.path.join(DIR_FILE, "file", "1.csv")
   # ReferenceDbAdapter = DbAdapter(lpath)
   # datos = ReferenceDbAdapter.get()
   user = {
            "id": "0",
            "name": "administrator",
            "is_authenticated": True,
   }
   # # VALUES IN FORMAT
   # # "id","write_at","value"
   # values = [float(item[2]) for item in datos if item]
   # nserial = [idx for idx in range(0,len(values))]
   # return render_template("index.html", title="index", values=values, nserial=nserial, current_user=user)
   return render_template("index.html", title="index", current_user=user)

@socketio.on('connect')
def connected():
   print('Connected')

@socketio.on('disconnect')
def disconnected():
   print('Disconnected')

# @app.route('/send_data', methods=['POST'])
@socketio.on('send_data')
def send_data(data):
   params = ["id", "write_at_str", "value"]
   # data = request.get_json()
   for item in params:
      if data.get(item) is None:
         raise KeyError(f"Invalid key {item}")
   json_data = dict()
   json_data["sensorid"] = data["id"]
   json_data["data"] = data["value"]
   json_data["write_at"] = datetime.strptime(data["write_at_str"], "%d/%m/%y %H:%M:%S")
   ReferenceSensor = SensorModel.from_dict(json_data)
   lpath = os.path.join(DIR_FILE, "file", str(json_data["sensorid"]) + ".csv")
   ReferenceDbAdapter = DbAdapter(lpath)
   ReferenceDbAdapter.save(ReferenceSensor.get_values())
   socketio.emit("draw", ReferenceSensor.data, broadcast=True)
   return json_data


if __name__ == "__main__":
   socketio.run(app)