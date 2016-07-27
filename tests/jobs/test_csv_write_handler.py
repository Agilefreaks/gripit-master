import unittest

from gripit.models.slave_reading import SlaveReading
from gripit.data.csv_write_handler import CsvWriteHandler
from mock import patch


class TestCsvWriteHandler(unittest.TestCase):
    @patch('gripit.services.logger.Logger', autospec=True)
    def setUp(self, MockLogger):
        self.mock_logger = MockLogger
        self.csv_write_handler = CsvWriteHandler()
        self.csv_write_handler.logger = self.mock_logger

    def test_handle_logs_readings(self):
        readings = [SlaveReading()]
        self.csv_write_handler.current_file_name = 'name'

        self.csv_write_handler.handle(readings)

        self.mock_logger.write.assert_called_with('name', readings)
