from random import random

class CarParkService():
    
    def check_status(self):
        number_car = round(random()*10, 0)
        return { 
            'status_sensor_1': 'AAAA',
            'status_sensor_2': 'BBBB',
            'car_number':number_car
            }