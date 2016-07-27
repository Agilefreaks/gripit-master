import csv
import os

from gripit.services.time_service import TimeService


class Logger:
    PATH = '/usr/local/gripit/logs/'
    FILE_EXTENSION = '.csv'

    def __init__(self):
        self.time_service = TimeService()

    def ensure_directory_exists(self):
        if not os.path.exists(Logger.PATH):
            os.makedirs(Logger.PATH)

    def create_new_file(self):
        self.ensure_directory_exists()
        file_name = str(self.time_service.current_milli_time()) + Logger.FILE_EXTENSION
        with open(Logger.PATH + file_name, 'w', newline='') as csvfile:
            csv.writer(csvfile)
        return file_name

    def write(self, file_name, slave_readings):
        with open(Logger.PATH + file_name, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=',', quotechar=';', quoting=csv.QUOTE_MINIMAL)

            for slave_reading in slave_readings:
                csv_writer.writerow([
                    slave_reading.slave_id,
                    slave_reading.time,
                    slave_reading.up,
                    slave_reading.right,
                    slave_reading.down,
                    slave_reading.left
                ])
