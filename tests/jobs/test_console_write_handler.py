import unittest

from mock import patch
from gripit.services.console import Console
from gripit.models.slave_reading import SlaveReading
from gripit.data.console_write_handler import ConsoleWriteHandler
from mock import patch


class TestConsoleWriteHandler(unittest.TestCase):
    def setUp(self):
        self.console_write_handler = ConsoleWriteHandler()

    @patch.object(Console, 'write')
    def test_handle_logs_readings(self, ConsoleWrite):
        readings = [SlaveReading(1, 2, 3, 4, 5, 6)]

        self.console_write_handler.handle(readings)

        ConsoleWrite.assert_called_with('SID: 1 ||| Time: 2 ||| Up: 3 ||| Right: 4 ||| Down: 5 ||| Left: 6')
