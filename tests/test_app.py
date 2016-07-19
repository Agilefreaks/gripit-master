import unittest
from gripit.app import App
from mock import patch, call


class TestApp(unittest.TestCase):
    @patch('gripit.gpio.service.GPIO', autospec=True)
    def setUp(self, MockGPIO):
        self.mock_gpio = MockGPIO()
        self.app = App(MockGPIO)
        self.led_pin = 2

    def tearDown(self):
        self.mock_gpio.reset_mock()

    def test_start_reading(self):
        self.app.start_reading()
        self.mock_gpio.output.assert_has_calls([call(self.led_pin, False)])

    def test_stop_reading(self):
        self.app.stop_reading()
        self.mock_gpio.output.assert_has_calls([call(self.led_pin, True)])

    def test_toggle_read(self):
        self.app._is_reading_data = True
        self.app.toggle_read()
        self.assertEqual(self.app._is_reading_data, False)
