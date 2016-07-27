import unittest
from gripit.services.gripit_modbus_client import GripitModbusClient


class TestSingletonModbusClient(unittest.TestCase):
    def test_call_always_returns_the_same_instance(self):
        modbus_client1 = GripitModbusClient()
        modbus_client2 = GripitModbusClient()
        self.assertIs(modbus_client1, modbus_client2)

    def test_instance_always_has_correct_config_arguments(self):
        client = GripitModbusClient()

        self.assertEqual("/dev/ttyUSB0", client.port)
        self.assertEqual("rtu", client.method)
