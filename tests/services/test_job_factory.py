import unittest

from mock import patch, PropertyMock

from gripit.services.job_factory import JobFactory
from gripit.data.console_write_handler import ConsoleWriteHandler
from gripit.data.csv_write_handler import CsvWriteHandler
from gripit.jobs.address_auto_assignment_job import AddressAutoAssignmentJob
from gripit.jobs.reading_job import ReadingJob


class TestJobFactory(unittest.TestCase):
    def setUp(self):
        self.job_factory = JobFactory()

    def test_create_reading_job_will_return_an_instance_of_a_reading_job(self):
        self.assertIsInstance(self.job_factory.create_reading_job(), ReadingJob)

    def test_create_reading_job_when_log_to_screen_is_true_sets_a_console_handler_on_the_job(self):
        with patch('gripit.services.job_factory.Config.log_data_to_screen', new_callable=PropertyMock, return_value=True):
            job = self.job_factory.create_reading_job()
        self.assertIsInstance(job.handler, ConsoleWriteHandler)

    def test_create_reading_job_when_log_to_screen_is_false_sets_a_csv_handler_on_the_job(self):
        with patch('gripit.services.job_factory.Config.log_data_to_screen', new_callable=PropertyMock, return_value=False):
            job = self.job_factory.create_reading_job()
        self.assertIsInstance(job.handler, CsvWriteHandler)

    def test_create_auto_assignment_job_will_return_an_instance_of_a_reading_job(self):
        self.assertIsInstance(self.job_factory.create_auto_assignment_job(), AddressAutoAssignmentJob)
