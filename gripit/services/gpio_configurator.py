from gripit.config import Config


class GPIOConfigrator:
    def __init__(self, GPIO):
        self.gpio = GPIO()

    def setup(self):
        self.set_mode()
        self.set_led_pin()
        self.set_button_pin()

    def set_mode(self):
        self.gpio.setmode(self.gpio.BCM)
        self.gpio.setwarnings(False)

    def set_led_pin(self):
        self.gpio.setup(Config.LED_PIN, self.gpio.OUT)

    def set_button_pin(self):
        self.gpio.setup(Config.BUTTON_PIN,
                        self.gpio.IN,
                        pull_up_down=self.gpio.PUD_UP)
