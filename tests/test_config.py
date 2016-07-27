import unittest

from gripit.config import Config


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = Config

    def test_default_log_data_to_screen_is_false(self):
        self.assertFalse(Config.log_data_to_screen)

    def test_max_readings_is_none(self):
        self.assertEqual(Config.max_readings_count, float('inf'))

    def test_sensors_to_read_contains_5_addresses(self):
        self.assertEqual(len(Config.sensors_to_read), 5)
