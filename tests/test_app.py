import unittest

from mock import patch

from gripit.app import App
from gripit.services.interaction_manager import InteractionManager


class TestApp(unittest.TestCase):
    @patch('gripit.app.ButtonHandler', autospec=True)
    @patch('gripit.app.JobFactory', autospec=True)
    @patch('gripit.app.JobRunner', autospec=True)
    @patch('gripit.services.gpio.GPIO', autospec=True)
    def setUp(self, MockGPIO, MockJobRunner, MockJobFactory, MockButtonHandler):
        self.mock_job_runner = MockJobRunner()
        self.mock_job_factory = MockJobFactory()
        self.mock_button_handler = MockButtonHandler(MockGPIO)

        self.app = App(MockGPIO)

    def test_run_when_start_immediately_is_true_will_start_read_job(self):
        self.app.config.start_immediately = True

        self.app.run()

        mock_job = self.mock_job_factory.create_reading_job()
        self.mock_job_runner.start.assert_called_with(mock_job)

    def test_run_when_start_auto_assignment_is_true_will_start_read_job(self):
        self.app.config.start_auto_assignment = True

        self.app.run()

        mock_job = self.mock_job_factory.create_auto_assignment_job()
        self.mock_job_runner.start.assert_called_with(mock_job)

    def test_run_when_in_interactive_mode_will_start_monitoring(self):
        self.app.run()

        self.mock_button_handler.start_monitoring.assert_called()

    def test_run_when_in_interactive_mode_adds_an_interaction_manager_to_the_button_handler_observers(self):
        self.app.run()

        self.mock_button_handler.add_observer.assert_called_once()

        first_argument = self.mock_button_handler.add_observer.call_args[0][0]
        self.assertIsInstance(first_argument, InteractionManager)
