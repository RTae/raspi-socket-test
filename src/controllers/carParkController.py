from src.services.carParkService import CarParkService
from threading import Thread, Event

cps = CarParkService()
thread_stop_event = Event()

def check_car_status(socketio):
    """
    Check car park status from RPIO and sent it through socket
    Ideally to be run in a separate thread?
    """
    while not thread_stop_event.isSet():
        socketio.emit('carParkStatus', cps.check_status(), namespace='/data')
        socketio.sleep(1)