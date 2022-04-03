from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread, Event
from random import random

__author__ = 'rtae'

app = Flask(__name__, template_folder='src/templates')
app.config['SECRET_KEY'] = 'secret!'

#turn the flask app into a socketio app
socketio = SocketIO(app, async_mode=None)

#random number Generator Thread
thread = Thread()
thread_stop_event = Event()

def check_car_status():
    """
    Check car park status from RPIO and sent it through socket
    Ideally to be run in a separate thread?
    """
    #infinite loop of magical random numbers
    while not thread_stop_event.isSet():
        number_car = round(random()*10, 0)
        socketio.emit('carParkStatus', {'status_sensor_1': 'AAAA', 'status_sensor_2': 'BBBB','car_number':number_car}, namespace='/data')
        socketio.sleep(1)


@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

@socketio.on('connect', namespace='/data')
def test_connect():
    # need visibility of the global thread object
    global thread
    print('Client connected')

    #Start the random number generator thread only if the thread has not been started before.
    if not thread.is_alive():
        print("Starting Thread")
        thread = socketio.start_background_task(check_car_status)

@socketio.on('disconnect', namespace='/data')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app)