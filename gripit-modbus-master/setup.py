import RPi.GPIO as GPIO
import time

class Setup:
	LED_PIN = 2
	BUTTON_PIN = 26

	FIRST_SLAVE_ADDRESS = 2
	LAST_SLAVE_ADDRESS = 3

	FIRST_REGISTER_ADDRESS = 1
	LAST_REGISTER_ADDRESS = 4

	MODBUS_CLIENT_KWARGS = {
		"method": "rtu",
		"stopbits": 1,
		"bytesize": 8,
		"parity": "N",
		"baudrate": 115200,
		"port": "/dev/ttyUSB0",
        "timeout": 0.02
	}

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		GPIO.setup(Setup.LED_PIN, GPIO.OUT)
		GPIO.setup(Setup.BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
