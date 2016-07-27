import time
import threading

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

    def start_blinking(self):
        self._its_blinking = True
        threading.Thread(target=self.led_blink).start()

    def stop_blinking(self):
        self._its_blinking = False

    def shouldBlink(self):
        return self._its_blinking

    def led_blink(self):
        while True:
            if self.shouldBlink():
                self.turn_on()
                time.sleep(0.25)
                self.turn_off()
                time.sleep(0.25)
            else:
                break
