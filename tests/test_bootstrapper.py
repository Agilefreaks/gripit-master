import unittest
import sys

from mock import patch

from gripit.bootstrapper import Bootstrapper
from gripit.config import Config
from gripit.services.gpio_configurator import GPIOConfigrator
from gripit.app import App


class TestBootstrapper(unittest.TestCase):
    def setUp(self):
        self.app_patcher = patch.object(App, 'run', return_value=13)
        self.app_patcher.start()
        self.addCleanup(self.app_patcher.stop)

        self.bootstrapper = Bootstrapper()

    def tearDown(self):
        Config.sensors_to_read = range(Config.FIRST_SLAVE_ADDRESS,
                                       Config.LAST_SLAVE_ADDRESS + 1)
        Config.max_readings_count = float('inf')
        Config.log_data_to_screen = False
        Config.start_immediately = False

    @patch('sys.exit', autospec=True)
    def test_run_with_bad_args_terminates_the_process(self, MockSysExit):
        testargs = ["prog", "-z"]

        with patch.object(sys, 'argv', testargs):
            self.bootstrapper.run()

        MockSysExit.assert_called_with(2)

    def test_run_with_sensors_arguments_will_update_config(self):
        testargs = ["prog", "-s 1,2,3"]

        with patch.object(sys, 'argv', testargs):
            self.bootstrapper.run()

        self.assertEqual(Config.sensors_to_read, [1, 2, 3])

    def test_run_with_readings_arguments_will_update_config(self):
        testargs = ["prog", "-r 110"]

        with patch.object(sys, 'argv', testargs):
            self.bootstrapper.run()

        self.assertEqual(Config.max_readings_count, 110)

    def test_run_with_debug_arguments_will_update_config(self):
        testargs = ["prog", "-l"]

        with patch.object(sys, 'argv', testargs):
            self.bootstrapper.run()

        self.assertEqual(Config.log_data_to_screen, True)

    def test_run_with_valid_arguments_will_run_app(self):
        self.bootstrapper.run()

        App.run.assert_called_once()

    def test_run_with_valid_arguments_will_setup_the_GPIO(self):
        with patch.object(GPIOConfigrator, 'setup', return_value=None) as MockSetup:
            self.bootstrapper.run()

        MockSetup.assert_called_once()

    def test_run_with_auto_assignment_arguments_will_update_config(self):
        testargs = ["prog", "-a"]

        with patch.object(sys, 'argv', testargs):
            self.bootstrapper.run()

        self.assertTrue(Config.start_auto_assignment)

    def test_run_with_argument_followed_by_other_argument_without_spaces_updates_config(self):
        testargs = ["prog", "-as5"]

        with patch.object(sys, 'argv', testargs):
            self.bootstrapper.run()

        self.assertTrue(Config.start_auto_assignment)
        self.assertEqual(Config.sensors_to_read, [5])
