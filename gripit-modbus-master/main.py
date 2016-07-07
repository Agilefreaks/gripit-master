import RPi.GPIO as GPIO
import time
import tornado.ioloop
import threading

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
		self.is_reading_data = False
		self.data_reader = None

	def should_stop_reading(self):
		return not self.is_reading_data
		
	def ensure_data_reader_exists(self):
		if self.data_reader == None:
			self.data_reader = DataReader(self.should_stop_reading)	
		
	def start_reading(self):
		LightIndicator.turnOn()
		self.ensure_data_reader_exists()
		thread = threading.Thread(target=lambda: self.data_reader.start())
		thread.start()
		print('Started new session')

	def stop_reading(self):
		LightIndicator.turnOff()
		print('Finished session')
		
	def toggle_read(self):
		self.is_reading_data = not self.is_reading_data
		if(self.is_reading_data):
			self.start_reading()
		else:
			self.stop_reading()
		
class Bootstrapper:
	def setup():
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(LED_PIN, GPIO.OUT)
		GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
		
	def start():
		Bootstrapper.setup()
		LightIndicator.turnOff()
		app = App()
		GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=lambda _: app.toggle_read(), bouncetime=500)
		while True:
			time.sleep(0.5)

Bootstrapper.start()