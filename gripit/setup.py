import time


class Setup:
    LED_PIN = 2
    BUTTON_PIN = 26

    FIRST_SLAVE_ADDRESS = 1
    LAST_SLAVE_ADDRESS = 5

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

    def __init__(self, GPIO):
        self.gpio = GPIO()

    def set(self):
        self.set_mode()
        self.set_led_pin()
        self.set_button_pin()

    def set_mode(self):
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setwarnings(False)

    def set_led_pin(self):
        self.gpio.setup(Setup.LED_PIN, self.gpio.OUT)

    def set_button_pin(self):
        self.gpio.setup(Setup.BUTTON_PIN,
                        self.gpio.IN,
                        pull_up_down=self.gpio.PUD_UP)
