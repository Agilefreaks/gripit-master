from gripit.config import Config
from gripit.services.gripit_modbus_client import GripitModbusClient
from gripit.jobs.job import Job
from gripit.services.reader import Reader


class ReadingJob(Job):
    def __init__(self, handler):
        self.client = GripitModbusClient()
        self.reader = Reader()
        self.handler = handler
        self.__is_stopped = False

    def is_running(self):
        return not self.__is_stopped

    def run(self):
        print('Started new session')
        self.__is_stopped = False
        self.client.connect()
        iterations = 0

        while self.is_running() and iterations < Config.max_readings_count:
            slave_readings = self.reader.read_slaves(Config.sensors_to_read)
            self.handler.handle(slave_readings)
            iterations += 1

        self.stop()
        print('Finished session')

    def stop(self):
        self.__is_stopped = True
        self.client.close()
