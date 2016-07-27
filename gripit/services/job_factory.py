from gripit.config import Config
from gripit.data.console_write_handler import ConsoleWriteHandler
from gripit.data.csv_write_handler import CsvWriteHandler
from gripit.jobs.address_auto_assignment_job import AddressAutoAssignmentJob
from gripit.jobs.reading_job import ReadingJob


class JobFactory:
    def create_reading_job(self):
        handler = ConsoleWriteHandler() if Config.log_data_to_screen else CsvWriteHandler()
        reading_job = ReadingJob(handler)

        return reading_job

    def create_auto_assignment_job(self):
        return AddressAutoAssignmentJob()
