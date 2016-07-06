import RPi.GPIO as GPIO
import time
import tornado.ioloop
import threading
import data_reader

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

LED_PIN = 2
BUTTON_PIN = 26

GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

IS_READING_DATA = False

def lightOn():
	GPIO.output(LED_PIN, False)

def lightOff():
	GPIO.output(LED_PIN, True)

def should_stop_reading():
	global IS_READING_DATA
	return not IS_READING_DATA
	
def start_reading():
	lightOn()
	thread = threading.Thread(target=lambda: data_reader.start(should_stop_reading))
	thread.start()
	print('Started new session')

def stop_reading():
	lightOff()
	print('Finished session')
	
def toggle_read():
	global IS_READING_DATA
	IS_READING_DATA = not IS_READING_DATA
	if(IS_READING_DATA):
		start_reading()
	else:
		stop_reading()

lightOff()
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=lambda _: toggle_read(), bouncetime=200)

while True:
	time.sleep(0.5)