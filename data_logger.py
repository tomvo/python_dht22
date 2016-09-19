#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import glob
sys.path.insert(0, '/home/pi/programs/libraries')

#global 
import time

#private
from lib.controller import Controller

controller = Controller(0.5, 5)

log_file = "/home/pi/programs/fridge_controller/log/temp_humid.log"
open(log_file, 'a').close()

while 1:
    controller.read()

    data = "{}: {} {} {:3.2f}".format(
        int(time.time()), controller.humidity, controller.temperature, controller.staleness)

    # print controller.get_status()

    print data
    with open(log_file, "a") as f:
      f.write(data + "\n")

    #if log file reaches certain length, rotate
    file_size = os.path.getsize(log_file)
    if file_size > (1000*500): #500k
        os.chdir( "/home/pi/programs/fridge_controller/log/" )
        current_index = 0
        for file in glob.glob('*.*'):
            ext = file[len(file) -1]
            if ext.isdigit() and int(ext) > current_index:
                current_index = int(ext)

        #rename current log file
        os.rename(log_file, log_file + "." + str(current_index + 1))

        #create an empty new one
        open(log_file, 'a').close()

    time.sleep(10)
