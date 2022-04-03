from src.controllers.carParkController import check_car_status
from src.utils.helpers.general.logging import setup_logging
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import logging


'''
SETUP
'''
setup_logging()

app = Flask(__name__, template_folder='src/templates')
socketio = SocketIO(app, async_mode=None)
thread = Thread()

'''
FLASK
'''
@app.route('/')
def index():
    #only by sending this page first will the client be connected to the socketio instance
    return render_template('index.html')

'''
SOCKETIO
'''
@socketio.on('connect', namespace='/data')
def test_connect():
    # need visibility of the global thread object
    global thread
    logging.info('Client connected')

    #Start the thread only if the thread has not been started before.
    if not thread.is_alive():
        logging.info("Starting Thread")
        thread = socketio.start_background_task(check_car_status, socketio)

@socketio.on('disconnect', namespace='/data')
def test_disconnect():
    logging.info('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)