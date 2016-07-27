from pymodbus.client.sync import ModbusSerialClient

from gripit.jobs.job import Job
from gripit.services.reader import Reader
from gripit.config import Config


class ReadingJob(Job):
    def __init__(self):
        self.config = Config()
        self.client = ModbusSerialClient(**self.config.MODBUS_CLIENT_KWARGS)
        self.reader = Reader(self.client)
        self.handlers = []
        self.__is_stopped = False

    def add_handler(self, handler):
        self.handlers.append(handler)

    def is_running(self):
        return not self.__is_stopped

    def run(self):
        print('Started new session')
        self.__is_stopped = False
        self.client.connect()
        iterations = 0

        while self.is_running() and iterations < self.config.max_readings_count:
            slave_readings = self.reader.read_slaves(self.config.sensors_to_read)

            for handler in self.handlers:
                handler.handle(slave_readings)

            iterations += 1

        self.stop()
        print('Finished session')

    def stop(self):
        self.__is_stopped = True
        self.client.close()
