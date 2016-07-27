import unittest
import threading
import sys

from mock import patch
from pymodbus.exceptions import ConnectionException, ModbusIOException
from gripit.data.handler import Handler
from gripit.jobs.reading_job import ReadingJob
from gripit.models.slave_reading import SlaveReading
from gripit.config import Config


class TestHandler(Handler):
    def __init__(self, iteration_count, job):
        self.job = job
        self.iteration_count = iteration_count
        self.current_iteration = 0

    def handle(self, slave_readings):
        self.current_iteration += 1
        if self.current_iteration >= self.iteration_count:
            self.job.stop()


class TestReadingJob(unittest.TestCase):
    @patch('gripit.services.reader.Reader', autospec=True)
    @patch('pymodbus.client.sync.ModbusSerialClient', autospec=True)
    def setUp(self, MockClient, MockReader):
        self.mock_client = MockClient
        self.mock_reader = MockReader
        self.mock_config = Config()

        self.job = ReadingJob()
        self.job.client = self.mock_client
        self.job.reader = self.mock_reader
        self.job.config = self.mock_config

    def test_run_connects_client(self):
        self.__limit_iterations(1)

        self.job.run()

        self.mock_client.connect.assert_called()

    def test_run_closes_client(self):
        self.__limit_iterations(1)

        self.job.run()

        self.mock_client.close.assert_called()

    def test_run_reads_sensors(self):
        self.mock_config.sensors_to_read = [42]
        self.__limit_iterations(1)

        self.job.run()

        self.mock_reader.read_slaves.assert_called_with([42])

    @patch('gripit.data.handler.Handler', autospec=True)
    def test_run_invokes_handlers_with_slave_readings(self, Handler):
        self.job.add_handler(Handler)
        slave_readings = [SlaveReading()]
        self.__limit_iterations(1)
        self.mock_reader.read_slaves.return_value = slave_readings

        self.job.run()

        Handler.handle.assert_called_with(slave_readings)

    @patch('gripit.data.handler.Handler', autospec=True)
    def test_run_reads_only_max_readings_count(self, Handler):
        self.job.add_handler(Handler)
        self.mock_config.max_readings_count = 5
        slave_readings = [SlaveReading()]
        self.mock_reader.read_slaves.return_value = slave_readings
        self.__limit_iterations(10)

        self.job.run()

        self.assertEquals(Handler.handle.call_count, 5)

    def test_run_stops_after_reading_max_readings_count(self):
        self.mock_config.max_readings_count = 5
        slave_readings = [SlaveReading()]
        self.mock_reader.read_slaves.return_value = slave_readings
        self.__limit_iterations(10)

        self.job.run()

        self.assertFalse(self.job.is_running())

    def __limit_iterations(self, iteration_count):
        self.job.add_handler(TestHandler(iteration_count, self.job))
