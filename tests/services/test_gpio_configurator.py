import unittest

from gripit.services.gpio_configurator import GPIOConfigrator
from mock import patch, call
from gripit.services.gpio import GPIO


class TestGPIOConfigurator(unittest.TestCase):
    @patch('gripit.services.gpio.GPIO', autospec=True)
    def setUp(self, MockGPIO):
        self.mock_gpio = MockGPIO()
        self.configurator = GPIOConfigrator(MockGPIO)

    def test_set_mode(self):
        self.configurator.set_mode()
        self.mock_gpio.setmode.assert_called_with(self.mock_gpio.BCM)

    def test_set_button_pin(self):
        self.configurator.set_button_pin()
        self.mock_gpio.setup.assert_called_with(
            26,
            self.mock_gpio.IN,
            pull_up_down=self.mock_gpio.PUD_UP
        )

    def test_set_led_pin(self):
        self.configurator.set_led_pin()
        self.mock_gpio.setup.assert_called_with(2, self.mock_gpio.OUT)
