import unittest
import os

from mock import patch

from gripit.services.logger import Logger


class TestLogger(unittest.TestCase):
    @patch('gripit.services.logger.TimeService', autospec=True)
    def setUp(self, MockTimeService):
        self.mock_time_service = MockTimeService()

        self.logger = Logger()

    def test_ensure_directory_exists(self):
        self.logger.ensure_directory_exists()

        self.assertTrue(os.path.exists(self.logger.PATH))

    def test_create_new_file(self):
        self.mock_time_service.current_milli_time.return_value = 45234543

        file_name = self.logger.create_new_file()

        self.assertEqual(file_name, '45234543.csv')
