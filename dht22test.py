import sys
sys.path.insert(0, '/home/pi/programs/libraries')
import pigpio
import DHT22
import time

#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(4, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

pi = pigpio.pi()

s = DHT22.sensor(pi, 4)

s.trigger()

time.sleep(0.2)

print("{} {} {:3.2f} {} {} {} {}".format(
   s.humidity(), s.temperature(), s.staleness(),
   s.bad_checksum(), s.short_message(), s.missing_message(),
   s.sensor_resets()))

s.cancel()

pi.stop()   
