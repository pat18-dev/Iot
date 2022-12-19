from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
   return render_template('index.html')

@socketio.on('connect')
def on_connect():
   # Generate some example data for the temperature sensor
   temperatures = [24.5, 25.1, 26.3, 27.7, 28.9]
   socketio.emit('temperature', temperatures)

if __name__ == '__main__':
   socketio.run(app)