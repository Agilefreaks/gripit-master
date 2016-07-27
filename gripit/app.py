from gripit.config import Config
from gripit.services.button_handler import ButtonHandler
from gripit.services.interaction_manager import InteractionManager
from gripit.services.job_runner import JobRunner
from gripit.services.job_factory import JobFactory


class App:
    def __init__(self, GPIO):
        self.config = Config()
        self.job_factory = JobFactory()
        self.job_runner = JobRunner()
        self.button_handler = ButtonHandler(GPIO)
        self.interaction_manager = InteractionManager(GPIO)

    def run(self):
        if self.config.start_immediately:
            self.job_runner.start(self.job_factory.create_reading_job())
        elif self.config.start_auto_assignment:
            self.job_runner.start(self.job_factory.create_auto_assignment_job())
        else:
            self.button_handler.add_observer(self.interaction_manager)
            self.button_handler.start_monitoring()
