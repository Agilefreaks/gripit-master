import RPi.GPIO as GPIO
import time

from setup import Setup
from light_indicator import LightIndicator
from data import Reader as DataReader


class App:
    def __init__(self):
        self._is_reading_data = False
        self.data_reader = DataReader()
        self.light_indicator = LightIndicator()
        self.setup = Setup()

    def start_reading(self):
        self.light_indicator.turnOn()
        self.data_reader.start()
        print('Started new session')

    def stop_reading(self):
        self.light_indicator.turnOff()
        self.data_reader.stop()
        print('Finished session')

    def on_button_pressed(self, button_pin):
        self.toggle_read()

    def toggle_read(self):
        self._is_reading_data = not self._is_reading_data
        if(self._is_reading_data):
            self.start_reading()
        else:
            self.stop_reading()

    def start(self):
        self.data_reader = DataReader()
        GPIO.add_event_detect(Setup.BUTTON_PIN, GPIO.FALLING, callback=self.on_button_pressed, bouncetime=500)
        while True: time.sleep(0.5)
