import unittest
from gripit.app import App

from mock import patch
from gripit.services.thread_factory import ThreadFactory
from gripit.services.async_job_runner import AsyncJobRunner
from gripit.jobs.job import Job


class TestAsyncJobRunner(unittest.TestCase):
    @patch('threading.Thread', autospec=True)
    @patch('gripit.jobs.job.Job', autospec=True)
    def setUp(self, MockJob, MockThread):
        self.mock_job = MockJob
        self.mock_thread = MockThread
        self.mock_thread.is_alive.return_value = True

        self.async_job_runner = AsyncJobRunner()

    @patch.object(ThreadFactory, 'create')
    def test_start_creates_new_thread(self, MockThreadCreate):
        MockThreadCreate.return_value = self.mock_thread

        self.async_job_runner.start(self.mock_job)

        MockThreadCreate.assert_called_with(self.mock_job.run)

    @patch.object(ThreadFactory, 'create')
    def test_start_creates_starts_thread(self, MockThreadCreate):
        MockThreadCreate.return_value = self.mock_thread

        self.async_job_runner.start(self.mock_job)

        self.mock_thread.start.assert_called()

    @patch.object(ThreadFactory, 'create')
    def test_stop_stops_job(self, MockThreadCreate):
        MockThreadCreate.return_value = self.mock_thread
        self.async_job_runner.start(self.mock_job)

        self.async_job_runner.stop(self.mock_job)

        self.mock_job.stop.assert_called()

    @patch.object(ThreadFactory, 'create')
    def test_stop_waits_for_thread(self, MockThreadCreate):
        MockThreadCreate.return_value = self.mock_thread
        self.async_job_runner.start(self.mock_job)

        self.async_job_runner.stop(self.mock_job)

        self.mock_thread.join.assert_called()

    @patch.object(ThreadFactory, 'create')
    def test_is_idle_when_job_is_running_returns_false(self, MockThreadCreate):
        MockThreadCreate.return_value = self.mock_thread
        self.async_job_runner.start(self.mock_job)

        self.async_job_runner.stop(self.mock_job)

        self.assertFalse(self.async_job_runner.is_idle())

    @patch.object(ThreadFactory, 'create')
    def test_is_idle_when_no_job_is_running_returns_true(self, MockThreadCreate):
        MockThreadCreate.return_value = self.mock_thread
        self.mock_thread.is_alive.return_value = False
        self.async_job_runner.start(self.mock_job)

        self.async_job_runner.stop(self.mock_job)

        self.assertTrue(self.async_job_runner.is_idle())
