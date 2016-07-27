from gripit.data.handler import Handler
from gripit.services.logger import Logger


class CsvWriteHandler(Handler):
    def __init__(self):
        self.logger = Logger()
        self.current_file_name = None

    def handle(self, slave_readings):
        file_name = self.__ensure_file()
        self.logger.write(file_name, slave_readings)

    def __ensure_file(self):
        if not self.current_file_name:
            self.current_file_name = self.logger.create_new_file()

        return self.current_file_name
