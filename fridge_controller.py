#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/home/pi/programs/libraries')

#global 
import time


#private
from lib.controller import Controller
#from lib.temperature import Temperature
#from lib.humidity import Humidity


#ask for target temp and humidty
# temperature.target = input("Specify target temperature:")
# humidity.target = input("Specify target humidity:")

target_temperature = 28
target_humidity = 80

controller = Controller(0.5, 5)

while 1:
    controller.read()

    controller.control_temperature(target_temperature)
    # controller.control_humidity(target_temp, target_humidity)

    data = "{}: {} {} {:3.2f}".format(
        int(time.time()), controller.humidity, controller.temperature, controller.staleness)

    print data
#    with open("temp_humid.log", "a") as f:
#        f.write(data + "\n")

    time.sleep(3)
