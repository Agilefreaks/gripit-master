import time
import unittest
from threading import Thread

from mock import patch, PropertyMock

from gripit.jobs.reading_job import ReadingJob
from gripit.models.slave_reading import SlaveReading


class TestReadingJob(unittest.TestCase):
    @patch('gripit.data.handler.Handler', autospec=True)
    @patch('gripit.jobs.reading_job.Reader', autospec=True)
    @patch('gripit.jobs.reading_job.GripitModbusClient', autospec=True)
    def setUp(self, MockClient, MockReader, MockHandler):
        self.mock_client = MockClient()
        self.mock_reader = MockReader()
        self.mock_handler = MockHandler()

        self.job = ReadingJob(self.mock_handler)

    def test_run_connects_client(self):
        self.__run_job()

        self.mock_client.connect.assert_called()

    def test_run_closes_client(self):
        self.__run_job()

        self.mock_client.close.assert_called()

    def test_run_reads_sensors(self):
        with patch('gripit.jobs.reading_job.Config.sensors_to_read', new_callable=PropertyMock, return_value=[42]):
            self.__run_job()

        self.mock_reader.read_slaves.assert_called_with([42])

    def test_run_invokes_handler_with_slave_readings(self):
        slave_readings = [SlaveReading()]
        self.mock_reader.read_slaves.return_value = slave_readings

        self.__run_job()

        self.mock_handler.handle.assert_called_with(slave_readings)

    def test_run_stops_after_reading_max_readings_count(self):
        slave_readings = [SlaveReading()]
        self.mock_reader.read_slaves.return_value = slave_readings
        with patch('gripit.jobs.reading_job.Config.max_readings_count', new_callable=PropertyMock, return_value=5):
            self.__run_job()

        self.assertEqual(self.mock_handler.handle.call_count, 5)

    def __run_job(self):
        self.thread = Thread(target=self.job.run)
        self.thread.start()
        time.sleep(0.1)
        self.job.stop()
