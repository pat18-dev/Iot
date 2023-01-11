import os
from datetime import datetime
import logging
import json
import random
import sys
import time
from typing import Iterator

from adapter.DbAdapter import DbAdapter
from model.SensorModel import SensorModel

from flask import (
    Flask,
    render_template,
    request,
    Response,
    session,
    stream_with_context,
)

logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret!"
app.config["PORT"] = 5000
DIR_FILE = os.path.join(os.path.dirname(__file__))
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
random.seed()  # Initialize the random number generator


def generate_random_data() -> Iterator[str]:
    """
    Generates random value between 0 and 100
    :return: String containing current timestamp (YYYY-mm-dd HH:MM:SS) and randomly generated data.
    """
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr or ""

    try:
        logger.info("Client %s connected", client_ip)
        while True:
            json_data = json.dumps(
                {
                    "time": datetime.now().strftime(DATE_FORMAT),
                    "value": random.randint(20, 30),
                }
            )
            yield f"data:{json_data}\n\n"
            time.sleep(1)
    except GeneratorExit:
        logger.info("Client %s disconnected", client_ip)


def get_data() -> Iterator[str]:
    if request.headers.getlist("X-Forwarded-For"):
        client_ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        client_ip = request.remote_addr or ""

    try:
        logger.info("Client %s connected", client_ip)
        lpath = os.path.join(DIR_FILE, "file", "1.csv")
        ReferenceDbAdapter = DbAdapter(lpath)
        db_data = ReferenceDbAdapter.get()[-1]
        print("---DATA")
        print(db_data)
        while True:
            json_data = json.dumps(
                {
                    "time": db_data[1],
                    "value": db_data[2],
                }
            )
            yield f"data:{json_data}\n\n"
            time.sleep(1)
    except GeneratorExit:
        logger.info("Client %s disconnected", client_ip)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/after")
def index_after():
    lpath = os.path.join(DIR_FILE, "file", "1.csv")
    ReferenceDbAdapter = DbAdapter(lpath)
    datos = ReferenceDbAdapter.get()
    user = {
        "id": "0",
        "name": "administrator",
        "is_authenticated": True,
    }
    # # VALUES IN FORMAT
    # # "id","write_at","value"
    values = [float(item[2]) for item in datos if item]
    nserial = [idx for idx in range(0, len(values))]
    return render_template(
        "index.html", title="index", values=values, nserial=nserial, current_user=user
    )


@app.route("/send_data", methods=["POST"])
def send_data():
    params = ["id", "write_at_str", "value"]
    data = request.get_json()
    for item in params:
        if data.get(item) is None:
            raise KeyError(f"Invalid key {item}")
    json_data = dict()
    json_data["sensorid"] = data["id"]
    json_data["data"] = data["value"]
    json_data["write_at"] = datetime.strptime(data["write_at_str"], DATE_FORMAT)
    ReferenceSensor = SensorModel.from_dict(json_data)
    lpath = os.path.join(DIR_FILE, "file", str(json_data["sensorid"]) + ".csv")
    ReferenceDbAdapter = DbAdapter(lpath)
    ReferenceDbAdapter.save(ReferenceSensor.get_values())
    return {"OK": 1}


@app.route("/chart-data")
def chart_data() -> Response:
    response = Response(stream_with_context(get_data()), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", threaded=True)
