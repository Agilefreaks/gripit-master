import unittest

from gripit.services.light_indicator import LightIndicator
from mock import patch, call


class TestLightIndicator(unittest.TestCase):
    @patch('gripit.services.gpio.GPIO', autospec=True)
    def setUp(self, MockGPIO):
        self.mock_gpio = MockGPIO()
        self.led_pin = 2

        self.light_indicator = LightIndicator(MockGPIO)

    def test_turn_on_will_set_low_gpio_led_pin(self):
        self.light_indicator.turn_on()

        self.mock_gpio.output.assert_has_calls([call(self.led_pin, False)])

    def test_turn_off_will_set_high_gpio_led_pin(self):
        self.light_indicator.turn_off()

        self.mock_gpio.output.assert_has_calls([call(self.led_pin, True)])
