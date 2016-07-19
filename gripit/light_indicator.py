import time
import threading

from gripit.setup import Setup


class LightIndicator:
    def __init__(self, GPIO):
        self.gpio = GPIO()
        self.turnOff()
        self._its_blinking = False

    def turnOn(self):
        self.gpio.output(Setup.LED_PIN, False)

    def turnOff(self):
        self.gpio.output(Setup.LED_PIN, True)

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
                self.turnOn()
                time.sleep(0.25)
                self.turnOff()
                time.sleep(0.25)
            else:
                break
