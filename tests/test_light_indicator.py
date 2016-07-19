import unittest

from gripit.light_indicator import LightIndicator
from mock import patch, call


class TestLightIndicator(unittest.TestCase):
    @patch('gripit.gpio.service.GPIO', autospec=True)
    def setUp(self, MockGPIO):
        self.mock_gpio = MockGPIO()
        self.light_indicator = LightIndicator(MockGPIO)
        self.led_pin = 2

    def tearDown(self):
        self.mock_gpio.reset_mock()

    def test_turn_on(self):
        self.light_indicator.turnOn()
        self.mock_gpio.output.assert_has_calls([call(self.led_pin, False)])

    def test_turn_off(self):
        self.light_indicator.turnOff()
        self.mock_gpio.output.assert_has_calls([call(self.led_pin, True)])

    def test_start_blinking(self):
        self.light_indicator._its_blinking = False
        self.light_indicator.start_blinking()
        self.assertEqual(self.light_indicator._its_blinking, True)

    def test_stop_blinking(self):
        self.light_indicator._its_blinking = True
        self.light_indicator.stop_blinking()
        self.assertEqual(self.light_indicator._its_blinking, False)

    def test_shouldBlink(self):
        self.light_indicator._its_blinking = True
        self.assertEqual(self.light_indicator.shouldBlink(), True)
