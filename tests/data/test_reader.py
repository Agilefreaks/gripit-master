import unittest

from mock import patch
from gripit.data import Reader

from gripit.setup import Setup
from pymodbus.register_read_message import ReadInputRegistersResponse


class TestReader(unittest.TestCase):
    @patch('pymodbus.client.sync.ModbusSerialClient', autospec=True)
    def setUp(self, mock_ModbusClient):
        self.reader = Reader()
        self.mock_ModbusClient = mock_ModbusClient

    def test_should_continue_initialy_will_be_false(self):
        self.assertEqual(self.reader.should_continue(), False)

    def test_sholud_continue_after_start_will_be_true(self):
        self.reader.start()
        self.assertEqual(self.reader.should_continue(), True)

    def test_read_input_registers(self):
        slave_id = 1
        self.reader.client = self.mock_ModbusClient
        self.reader.read_input_registers(slave_id)
        self.assertTrue(self.mock_ModbusClient.read_input_registers.called)

    def test_create_client(self):
        self.reader.create_client(self.mock_ModbusClient)
        self.assertTrue(self.mock_ModbusClient.connect.called)

    def test_ensure_client_exists(self):
        self.reader.client = None
        self.reader.MODBUS_CLIENT = self.mock_ModbusClient
        self.reader.ensure_client_exists()
        self.assertTrue(self.mock_ModbusClient.connect.called)

    def test_read_slave_registers(self):
        slave_id = 1
        self.reader.client = self.mock_ModbusClient
        response = self.reader.read_input_registers(slave_id)
        self.assertEqual(self.reader.read_slave_registers(slave_id), response)

    @patch('gripit.data.logger.Logger', autospec=True)
    def test_handle_response_when_have_valid_registers(self, mock_Logger):
        slave_id = 1
        self.reader.logger = mock_Logger
        self.reader.client = self.mock_ModbusClient
        self.reader.current_file_name = 'name'
        registers = self.reader.read_slave_registers(slave_id)
        self.reader.handle_response(registers, slave_id)
        mock_Logger.write.assert_called_with('name',
                                             registers.registers,
                                             slave_id)

    @patch('gripit.data.logger.Logger', autospec=True)
    def test_handle_response_when_not_have_valid_registers(self, mock_Logger):
        slave_id = 1
        self.reader.logger = mock_Logger
        self.reader.client = self.mock_ModbusClient
        self.reader.current_file_name = 'name'
        registers = None
        self.reader.handle_response(registers, slave_id)
        mock_Logger.write.assert_called_with('name',
                                             [-1, -1, -1, -1],
                                             slave_id)

    @patch('gripit.data.logger.Logger', autospec=True)
    def test_write_registers(self, mock_Logger):
        slave_id = 1
        self.reader.logger = mock_Logger
        self.reader.client = self.mock_ModbusClient
        registers = self.reader.read_slave_registers(slave_id)
        self.reader.write_registers(registers, slave_id)
        self.assertTrue(mock_Logger.write.called)

    def test_stop(self):
        self.reader._is_started = True
        self.reader.stop()
        self.assertEqual(self.reader._is_started, False)

    def test_start(self):
        self.reader._is_started = False
        self.reader.start()
        self.assertEqual(self.reader._is_started, True)

if __name__ == '__main__':
    unittest.main()
