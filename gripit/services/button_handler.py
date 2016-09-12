import time
from decimal import Decimal

from gripit.config import Config
from gripit.exceptions.invalid_observer_exception import InvalidObserverException

from gripit.core.button_observer import ButtonObserver
from gripit.services.job_runner import JobRunner
from gripit.services.thread_factory import ThreadFactory


class ButtonHandler:
    def __init__(self, GPIO):
        self.gpio = GPIO()
        self.job_runner = JobRunner()

        self.__dispose_callback = None
        self.__bounce_time = 500

        self.observers = list()
        self.pressed = False
        self.initial_press_time = 0

    def start_monitoring(self):
        self.__dispose_callback = self.__monitor_button_pin()
        return self.__dispose_callback

    def add_observer(self, observer):
        if isinstance(observer, ButtonObserver):
            self.observers.append(observer)
        else:
            raise InvalidObserverException()

    def __notify_observers(self, press_time):
        for observer in self.observers:
            observer.update(press_time)

    def __on_button_pressed(self, _):
        if self.pressed:
            press_time = Decimal(time.time() - self.initial_press_time)
            self.initial_press_time = 0
            self.pressed = False
            self.__notify_observers(press_time)
        else:
            self.initial_press_time = time.time()
            self.pressed = True

    def __monitor_button_pin(self):
        keep_monitoring = True
        button_handler = self

        def stop_monitoring_callback():
            nonlocal keep_monitoring
            keep_monitoring = False

        def monitor_loop():
            nonlocal keep_monitoring, button_handler
            button_handler.gpio.add_event_detect(Config.BUTTON_PIN, self.gpio.BOTH,
                                                 callback=button_handler.__on_button_pressed,
                                                 bouncetime=button_handler.__bounce_time)
            while keep_monitoring:
                time.sleep(0.5)

        ThreadFactory.create(monitor_loop).start()

        return stop_monitoring_callback
