import time

from gripit.config import Config
from gripit.services.light_indicator import LightIndicator
from gripit.jobs.reading_job import ReadingJob
from gripit.services.job_factory import JobFactory
from gripit.data.console_write_handler import ConsoleWriteHandler
from gripit.data.csv_write_handler import CsvWriteHandler
from gripit.services.async_job_runner import AsyncJobRunner


class App:
    def __init__(self, GPIO):
        self.gpio = GPIO()
        self.config = Config()
        self.reading_job = None
        self.job_runner = AsyncJobRunner()
        self.light_indicator = LightIndicator(GPIO)

    def start_reading(self):
        self.light_indicator.turn_on()
        self.reading_job = self.__create_reading_job()
        self.job_runner.start(self.reading_job)

    def stop_reading(self):
        self.light_indicator.turn_off()
        self.job_runner.stop(self.reading_job)
        self.reading_job = None

    def on_button_pressed(self, button_pin):
        self.toggle_read()

    def toggle_read(self):
        if self.job_runner.is_idle():
            self.start_reading()
        else:
            self.stop_reading()

    def start(self):
        if self.config.start_immediately:
            self.start_reading()
        else:
            self.gpio.add_event_detect(self.config.BUTTON_PIN, self.gpio.FALLING,
                                       callback=self.on_button_pressed, bouncetime=500)

    def keep_alive(self):
        return not self.config.start_immediately or not self.job_runner.is_idle()

    def run(self):
        self.start()

        while self.keep_alive():
            time.sleep(0.5)

    def __create_reading_job(self):
        reading_job = JobFactory.create(ReadingJob)
        reading_job.add_handler(CsvWriteHandler())

        if self.config.log_data_to_screen:
            reading_job.add_handler(ConsoleWriteHandler())

        return reading_job
