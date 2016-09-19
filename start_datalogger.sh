#!/bin/sh

sudo pigpiod

python /home/pi/programs/fridge_controller/data_logger.py &
