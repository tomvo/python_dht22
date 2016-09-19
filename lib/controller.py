import pigpio
import DHT22
import time

class Controller:
    CONTROLLING_IDLE = 0
    CONTROLLING_DOWN = 1
    CONTROLLING_UP = 2

    def __init__(self, temperature_tolerance, humidity_tolerance):
        self.pi = pigpio.pi()
        self.sensor = DHT22.sensor(self.pi, 21)

        self.controlling_state_temperature = self.CONTROLLING_IDLE
        self.controlling_state_humidity = self.CONTROLLING_IDLE
        
        self.temperature_tolerance = temperature_tolerance
        self.humidity_tolerance = humidity_tolerance

        self.temperature = -1
        self.humidity = -1
        self.staleness = -1

    def get_status(self):
        data = "{} {} {:3.2f} {} {} {} {}".format(
         self.sensor.humidity(), self.sensor.temperature(), self.sensor.staleness(),
         self.sensor.bad_checksum(), self.sensor.short_message(), self.sensor.missing_message(),
         self.sensor.sensor_resets())

	return data


    def read(self):
        self.sensor.trigger()

        time.sleep(0.2)

        if self.sensor.temperature() < 0:
            return 
        else:
            self.temperature = self.sensor.temperature()
            self.humidity = self.sensor.humidity()
            self.staleness = self.sensor.staleness()

    def current_temperature(self):
        return self.temperature

    def current_humidity(self):
        return self.temperature

    def toggle_fridge(self, state):
        if state == 'on':
            print "turning on fridge"
        elif  state == 'off':
            print "turning off fridge"
        else:
            print "invalid state for fridge toggle"

    def control_temperature(self, target):
        if self.temperature == -1:
            return False

        print "Comparing temp: %f %f" % (self.temperature, target - self.temperature_tolerance)

        if self.controlling_state_temperature == self.CONTROLLING_IDLE:
            if self.temperature < (target - self.temperature_tolerance):
                self.controlling_state_temperature = self.CONTROLLING_UP
                self.toggle_fridge('off')
            elif self.temperature > (target + self.temperature_tolerance):
                self.controlling_state_temperature = self.CONTROLLING_DOWN
                self.toggle_fridge('on')

        elif  self.controlling_state_temperature == self.CONTROLLING_UP:
            #when controlling up state it means the fridge is off, we want the temp to rise
            #as soon as it reaches desired temperature, switch to idle mode
            if self.temperature > target:
                self.controlling_state_temperature = self.CONTROLLING_IDLE
                self.toggle_fridge('on')

        elif  self.controlling_state_temperature == self.CONTROLLING_DOWN:
            #when controlling down state it means the fridge is on, we want the fridge to be off
            #as soon as it reaches desired temperature, switch to idle mode
            if self.temperature < target:
                self.controlling_state_temperature = self.CONTROLLING_IDLE
                self.toggle_fridge('off')

    def end(self):
        self.sensor.cancel()
        self.pi.stop()

    def __exit__(self, exc_type, exc_value, traceback):
        self.sensor.cancel()
        self.pi.stop()
