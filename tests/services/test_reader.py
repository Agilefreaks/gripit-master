import unittest
import sys

from mock import patch

from gripit.models.slave_reading import SlaveReading
from pymodbus.exceptions import ConnectionException, ModbusIOException
from gripit.services.reader import Reader


class TestReader(unittest.TestCase):
    @patch('gripit.services.reader.TimeService', autospec=True)
    @patch('gripit.services.reader.GripitModbusClient', autospec=True)
    def setUp(self, MockClient, MockTimeService):
        self.mock_client = MockClient()
        self.mock_time_service = MockTimeService()

        self.reader = Reader()

    def test_read_slave_registers_reads_register_values(self):
        slave_id = 1
        self.mock_client.read_holding_registers.return_value = None

        self.reader.read_slave(slave_id)

        self.mock_client.read_holding_registers.assert_called_with(address=1,
                                                                 count=4,
                                                                 unit=slave_id)

    def test_read_slave_registers_when_client_returns_valid_registers(self):
        slave_id = 1
        self.mock_client.read_holding_registers.return_value = None
        self.mock_time_service.current_milli_time.return_value = 42

        result = self.reader.read_slave(slave_id)

        self.assertTrue(isinstance(result, SlaveReading))
        self.assertEqual(result.slave_id, slave_id)
        self.assertEqual(result.time, 42)
        self.assertEqual(result.up, -1)
        self.assertEqual(result.right, -1)
        self.assertEqual(result.down, -1)
        self.assertEqual(result.left, -1)

    @patch('pymodbus.register_read_message.ReadInputRegistersResponse', autospec=True)
    def test_read_registers_when_invalid_registers(self, MockResponse):
        slave_id = 1
        MockResponse.registers = [1, 2, 3, 4]
        self.mock_client.read_holding_registers.return_value = MockResponse
        self.mock_time_service.current_milli_time.return_value = 42

        result = self.reader.read_slave(slave_id)

        self.assertTrue(isinstance(result, SlaveReading))
        self.assertEqual(result.slave_id, slave_id)
        self.assertEqual(result.time, 42)
        self.assertEqual(result.up, 1)
        self.assertEqual(result.right, 2)
        self.assertEqual(result.down, 3)
        self.assertEqual(result.left, 4)

    @patch.object(sys, 'exit')
    def test_read_slave_registers_on_ConnectionException_exits(self, MockExit):
        slave_id = 1
        self.mock_client.read_holding_registers.side_effect = ConnectionException()

        self.reader.read_slave(slave_id)

        MockExit.assert_called()

    @patch.object(sys, 'exit')
    def test_read_slave_registers_on_ModbusIOException_exits(self, MockExit):
        slave_id = 1
        self.mock_client.read_holding_registers.side_effect = ModbusIOException()

        self.reader.read_slave(slave_id)

        MockExit.assert_called()
