import unittest

from mock import patch

from gripit.services.job_runner import JobRunner
from gripit.services.thread_factory import ThreadFactory


class TestJobRunner(unittest.TestCase):
    @patch('gripit.jobs.job.Job', autospec=True)
    @patch('threading.Thread', autospec=True)
    def setUp(self, MockJob, MockThread):
        self.mock_job = MockJob
        self.mock_thread = MockThread

        self.job_runner = JobRunner()

    def test_start_will_raise_exception_if_thread_already_started(self):
        self.job_runner.start(self.mock_job)

        with self.assertRaises(Exception) as cm:
            self.job_runner.start(self.mock_job)

        self.assertIsNotNone(cm.exception)

    @patch.object(ThreadFactory, 'create')
    def test_start_will_create_a_new_thread(self, MockThreadFactoryCreate):
        self.job_runner.start(self.mock_job)

        MockThreadFactoryCreate.assert_called_with(self.mock_job.run)

    @patch.object(ThreadFactory, 'create')
    def test_start_will_start_the_new_thread(self, MockThreadFactoryCreate):
        MockThreadFactoryCreate.return_value = self.mock_job

        self.job_runner.start(self.mock_job)

        self.mock_job.start.assert_called()

    @patch.object(ThreadFactory, 'create')
    def test_stop_will_stop_the_thread(self, MockThreadFactoryCreate):
        MockThreadFactoryCreate.return_value = self.mock_job
        self.job_runner.start(self.mock_thread)

        self.job_runner.stop()

        self.mock_thread.stop.assert_called()

    def test_is_idle_will_return_true_by_default(self):
        self.assertTrue(self.job_runner.is_idle())

    def test_is_idle_will_return_false_if_job_was_started(self):
        self.job_runner.start(self.mock_job)

        self.assertFalse(self.job_runner.is_idle())

    def test_is_busy_will_return_false_by_default(self):
        self.assertFalse(self.job_runner.is_busy())

    def test_is_busy_will_return_true_if_job_was_started(self):
        self.job_runner.start(self.mock_job)

        self.assertTrue(self.job_runner.is_busy())
