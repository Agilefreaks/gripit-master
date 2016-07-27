import time
import unittest
from _pydecimal import Decimal, ROUND_DOWN, Context
from threading import Thread

from mock import patch, ANY, PropertyMock

from gripit.exceptions.invalid_observer_exception import InvalidObserverException
from gripit.services.button_handler import ButtonHandler
from gripit.services.thread_factory import ThreadFactory


class TestButtonHandler(unittest.TestCase):
    @patch('gripit.services.gpio.GPIO', autospec=True)
    def setUp(self, MockGPIO):
        self.dispose_callback = None
        self.mock_gpio = MockGPIO()

        create_thread_patcher = patch.object(ThreadFactory, 'create')
        self.mock_create_thread = create_thread_patcher.start()
        self.addCleanup(create_thread_patcher.stop)

        self.button_handler = ButtonHandler(MockGPIO)

    def tearDown(self):
        if self.dispose_callback:
            self.dispose_callback()

    @patch('gripit.core.button_observer.ButtonObserver', autospec=True)
    def test_add_observer_will_push_given_observer_to_observers(self, MockButtonObserver):
        mock_observer = MockButtonObserver()

        self.button_handler.add_observer(mock_observer)

        self.assertEqual(self.button_handler.observers, [mock_observer])

    @patch('gripit.core.button_observer.ButtonObserver', autospec=True)
    def test_add_observer_called_subsequently_does_not_replace_previous_observers(self, MockButtonObserver):
        mock_observer1 = MockButtonObserver()
        mock_observer2 = MockButtonObserver()

        self.button_handler.add_observer(mock_observer1)
        self.button_handler.add_observer(mock_observer2)

        self.assertEqual(self.button_handler.observers, [mock_observer1, mock_observer2])

    def test_add_observer_will_raise_an_error_if_given_arg_will_not_be_an_observer(self):
        with self.assertRaises(InvalidObserverException) as cm:
            self.button_handler.add_observer('asd')
        self.assertIsInstance(cm.exception, InvalidObserverException)

    def test_start_monitoring_starts_a_new_thread(self):
        self.dispose_callback = self.button_handler.start_monitoring()

        self.mock_create_thread.assert_called_once()

    def test_start_monitoring_adds_a_gpio_handler_on_the_new_thread(self):
        self.__enable_thread_creation()

        self.dispose_callback = self.button_handler.start_monitoring()

        self.mock_gpio.add_event_detect.assert_called_once()

    def test_start_monitoring_adds_a_gpio_handler_on_the_new_thread_for_both_edges_on_the_configured_button_pin(self):
        self.__enable_thread_creation()
        mock_button_pin = 1313454

        with patch('gripit.config.Config.BUTTON_PIN', new_callable=PropertyMock, return_value=mock_button_pin):
            self.dispose_callback = self.button_handler.start_monitoring()

        self.mock_gpio.add_event_detect.assert_called_once_with(mock_button_pin, self.mock_gpio.BOTH,
                                                                callback=ANY, bouncetime=ANY)

    @patch('gripit.core.button_observer.ButtonObserver', autospec=True)
    def test_start_monitoring_observer_exists_and_a_button_is_pressed_and_released_calls_the_update_method(self,
                                                                                                           MockButtonObserver):
        button_press_time = Decimal('0.1')
        mock_observer = MockButtonObserver()
        self.button_handler.add_observer(mock_observer)
        self.__mock_button_press(button_press_time)
        self.__enable_thread_creation()

        self.dispose_callback = self.button_handler.start_monitoring()

        time.sleep(float(button_press_time) + 0.02)
        first_call = mock_observer.update.call_args[0]
        first_argument = first_call[0]
        self.assertEqual(Context(prec=1, rounding=ROUND_DOWN).create_decimal(first_argument), button_press_time)

    def __enable_thread_creation(self):
        self.mock_create_thread.side_effect = lambda callback: Thread(target=callback)

    def __mock_button_press(self, press_duration, sleep_time=0):
        def mock_add_event_detect(button_pin, edge, callback, bouncetime):
            callback(button_pin)
            time.sleep(float(press_duration))
            callback(button_pin)
            time.sleep(float(sleep_time))

        self.mock_gpio.add_event_detect.side_effect = mock_add_event_detect
