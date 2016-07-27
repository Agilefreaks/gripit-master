from gripit.services.console import Console
from gripit.data.handler import Handler


class ConsoleWriteHandler(Handler):
    def handle(self, slave_readings):
        for slave_reading in slave_readings:
            self.__print_reading(slave_reading)

    def __print_reading(self, slave_reading):
        reading_values = [
            slave_reading.slave_id,
            slave_reading.time,
            slave_reading.up,
            slave_reading.right,
            slave_reading.down,
            slave_reading.left
        ]

        Console.write('SID: {0} ||| Time: {1} ||| Up: {2} ||| Right: {3} ||| Down: {4} ||| Left: {5}'.format(*reading_values))
