import unittest
import os

from gripit.services.logger import Logger
from gripit.services.time_service import TimeService
from mock import patch


class TestLogger(unittest.TestCase):
    @patch('gripit.services.time_service.TimeService', autospec=True)
    def setUp(self, MockTimeService):
        self.mock_time_service = MockTimeService

        self.logger = Logger()
        self.logger.time_service = MockTimeService

    def test_ensure_directory_exists(self):
        self.logger.ensure_directory_exists()

        self.assertTrue(os.path.exists(self.logger.PATH))

    def test_create_new_file(self):
        self.mock_time_service.current_milli_time.return_value = 45234543

        file_name = self.logger.create_new_file()

        self.assertEqual(file_name, '45234543.csv')
