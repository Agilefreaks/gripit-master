import unittest

from mock import patch, call
from gripit.data.csv_write_handler import CsvWriteHandler
from gripit.data.console_write_handler import ConsoleWriteHandler
from gripit.jobs.reading_job import ReadingJob
from gripit.services.job_factory import JobFactory
from gripit.app import App
from tests.matchers.any_instance import AnyInstance


class TestApp(unittest.TestCase):
    @patch('gripit.config.Config', autospec=True)
    @patch('gripit.services.async_job_runner.AsyncJobRunner', autospec=True)
    @patch('gripit.services.light_indicator.LightIndicator', autospec=True)
    @patch('gripit.services.gpio.GPIO', autospec=True)
    def setUp(self, MockGPIO, MockLightIndicator, MockAsyncJobRunner, MockConfig):
        self.mock_gpio = MockGPIO
        self.mock_light_indicator = MockLightIndicator
        self.mock_async_job_runner = MockAsyncJobRunner
        self.mock_config = MockConfig

        self.app = App(MockGPIO)
        self.app.job_runner = self.mock_async_job_runner
        self.app.gpio = self.mock_gpio
        self.app.light_indicator = self.mock_light_indicator
        self.app.config = self.mock_config
        self.led_pin = 2

    def test_toggle_read_job_is_not_running_switches_light_on(self):
        self.mock_async_job_runner.is_idle.return_value = True

        self.app.toggle_read()

        self.mock_light_indicator.turn_on.assert_called()

    def test_toggle_read_job_is_not_running_starts_job(self):
        self.mock_async_job_runner.is_idle.return_value = True

        self.app.toggle_read()

        self.mock_async_job_runner.start.assert_called_with(AnyInstance(ReadingJob))

    def test_toggle_read_job_is_running_stops_job(self):
        self.mock_async_job_runner.is_idle.return_value = False
        self.app.start_reading()

        self.app.toggle_read()

        self.mock_async_job_runner.stop.assert_called_with(AnyInstance(ReadingJob))

    def test_toggle_read_job_is_running_stops_job(self):
        self.mock_async_job_runner.is_idle.return_value = False
        self.app.start_reading()

        self.app.toggle_read()

        self.mock_async_job_runner.stop.assert_called_with(AnyInstance(ReadingJob))

    def test_toggle_read_job_is_running_switches_light_off(self):
        self.mock_async_job_runner.is_idle.return_value = False

        self.app.toggle_read()

        self.mock_light_indicator.turn_off.assert_called()

    def test_start_start_immediately_is_true_starts_reading(self):
        self.mock_config.start_immediately = True

        self.app.start()

        self.mock_async_job_runner.start.assert_called_with(AnyInstance(ReadingJob))

    def test_start_start_immediately_is_false_does_not_start_reading(self):
        self.mock_config.start_immediately = False

        self.app.start()

        self.mock_async_job_runner.start.assert_not_called()

    @patch('gripit.jobs.reading_job.ReadingJob', autospec=True)
    @patch.object(JobFactory, 'create')
    def test_start_adds_csv_write_handler_to_reader(self, JobCreate, MockReadingJob):
        JobCreate.return_value = MockReadingJob

        self.app.start()

        MockReadingJob.add_handler.assert_any_call(AnyInstance(CsvWriteHandler))

    @patch('gripit.jobs.reading_job.ReadingJob', autospec=True)
    @patch.object(JobFactory, 'create')
    def test_start_log_to_screen_is_true_adds_console_write_handler_to_reader(self, JobCreate, MockReadingJob):
        JobCreate.return_value = MockReadingJob
        self.mock_config.log_data_to_screen = True

        self.app.start()

        MockReadingJob.add_handler.assert_any_call(AnyInstance(ConsoleWriteHandler))

    @patch('gripit.jobs.reading_job.ReadingJob', autospec=True)
    @patch.object(JobFactory, 'create')
    def test_start_log_to_screen_is_false_does_not_add_console_write_handler_to_reader(self, JobCreate, MockReadingJob):
        JobCreate.return_value = MockReadingJob
        self.mock_config.log_data_to_screen = False

        self.app.start()

        MockReadingJob.add_handler.assert_called_once_with(AnyInstance(CsvWriteHandler))

    def test_keep_alive_start_immediately_is_false_returns_true(self):
        self.mock_config.start_immediately = False

        result = self.app.keep_alive()

        self.assertTrue(result)

    def test_keep_alive_start_immediately_is_true_returns_false(self):
        self.mock_config.start_immediately = True

        result = self.app.keep_alive()

        self.assertFalse(result)

    def test_keep_alive_start_immediately_is_true_and_job_is_running_returns_true(self):
        self.mock_config.start_immediately = True
        self.mock_async_job_runner.is_idle.return_value = False

        result = self.app.keep_alive()

        self.assertTrue(result)

    def test_keep_alive_start_immediately_is_true_and_job_is_not_running_returns_false(self):
        self.mock_config.start_immediately = True
        self.mock_async_job_runner.is_idle.return_value = True

        result = self.app.keep_alive()

        self.assertFalse(result)
