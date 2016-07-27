import unittest

from mock import patch

from gripit.services.interaction_manager import InteractionManager


class TestInteractionManager(unittest.TestCase):
    @patch('gripit.services.interaction_manager.LightIndicator', autospec=True)
    @patch('gripit.services.interaction_manager.JobFactory', autospec=True)
    @patch('gripit.services.interaction_manager.JobRunner', autospec=True)
    @patch('gripit.services.gpio.GPIO', autospec=True)
    def setUp(self, MockGPIO, MockJobRunner, MockJobFactory, MockLightIndicator):
        self.mock_light_indicator = MockLightIndicator(MockGPIO)
        self.mock_job_runner = MockJobRunner()
        self.mock_job_factory = MockJobFactory()

        self.interaction_manager = InteractionManager(MockGPIO)

    def test_update_will_create_and_start_reading_job_if_press_time_is_not_longer_then_3_seconds(self):
        press_time = 2

        self.interaction_manager.update(press_time)

        self.mock_job_factory.create_reading_job.assert_called()
        self.mock_job_runner.start.assert_called_with(self.mock_job_factory.create_reading_job())

    def test_update_will_create_and_start_address_auto_assignment_job_if_press_time_is_longer_then_3_seconds(self):
        press_time = 5

        self.interaction_manager.update(press_time)

        self.mock_job_factory.create_auto_assignment_job.assert_called()
        self.mock_job_runner.start.assert_called_with(self.mock_job_factory.create_auto_assignment_job())

    def test_update_will_stop_reading_job_if_job_already_running(self):
        press_time = 3
        self.mock_job_runner.is_idle.return_value = False

        self.interaction_manager.update(press_time)

        self.mock_job_runner.stop.assert_called()

    def test_update_will_turn_on_light_if_job_not_already_running(self):
        press_time = 2

        self.interaction_manager.update(press_time)

        self.mock_light_indicator.turn_on.assert_called()

    def test_update_will_turn_off_light_if_job_already_running(self):
        press_time = 2
        self.mock_job_runner.is_idle.return_value = False

        self.interaction_manager.update(press_time)

        self.mock_light_indicator.turn_off.assert_called()
