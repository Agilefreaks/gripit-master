import RPi.GPIO as GPIO
import time
import tornado.ioloop

from data import AsyncReader as DataReader

LED_PIN = 2
BUTTON_PIN = 26

class LightIndicator:
	def turnOn():
		GPIO.output(LED_PIN, False)

	def turnOff():
		GPIO.output(LED_PIN, True)

class App:
	def __init__(self):
		self.__is_reading_data = False
		self.data_reader = None

	def start_reading(self):
		LightIndicator.turnOn()
		self.data_reader.start()
		print('Started new session')

	def stop_reading(self):
		LightIndicator.turnOff()
		self.data_reader.stop()
		print('Finished session')
		
	def toggle_read(self):
		self.__is_reading_data = not self.__is_reading_data
		if(self.__is_reading_data): self.start_reading()
		else: self.stop_reading()

	def start(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(LED_PIN, GPIO.OUT)
		GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		LightIndicator.turnOff()
		self.data_reader = DataReader()
		GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=self.toggle_read, bouncetime=500)
		while True: time.sleep(0.5)
		
App().start()