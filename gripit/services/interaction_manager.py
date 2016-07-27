from gripit.core.button_observer import ButtonObserver
from gripit.services.job_factory import JobFactory
from gripit.services.job_runner import JobRunner
from gripit.services.light_indicator import LightIndicator


class InteractionManager(ButtonObserver):
    def __init__(self, GPIO):
        self.__current_job = None

        self.light_indicator = LightIndicator(GPIO)
        self.job_runner = JobRunner()
        self.job_factory = JobFactory()

    def update(self, press_time):
        if self.job_runner.is_idle():
            self.__current_job = self.__get_job_by_press_time(press_time)
            self.__start_job()
        else:
            self.__stop_job()
            self.__current_job = None

    def __start_job(self):
        self.light_indicator.turn_on()
        self.job_runner.start(self.__current_job)

    def __stop_job(self):
        self.light_indicator.turn_off()
        self.job_runner.stop(self.__current_job)

    def __get_job_by_press_time(self, press_time):
        return self.job_factory.create_reading_job() \
            if press_time < 3 \
            else self.job_factory.create_auto_assignment_job()
