from gripit.config import Config


class LightIndicator:
    def __init__(self, GPIO):
        self.gpio = GPIO()
        self.turn_off()
        self._its_blinking = False

    def turn_on(self):
        self.gpio.output(Config.LED_PIN, False)

    def turn_off(self):
        self.gpio.output(Config.LED_PIN, True)
