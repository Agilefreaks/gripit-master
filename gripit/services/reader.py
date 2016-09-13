import sys

from gripit.config import Config
from pymodbus.exceptions import ConnectionException, ModbusIOException
from gripit.models.slave_reading import SlaveReading
from gripit.services.gripit_modbus_client import GripitModbusClient
from gripit.services.time_service import TimeService


class Reader:
    def __init__(self):
        self.client = GripitModbusClient()
        self.time_service = TimeService()

    def read_slaves(self, slave_ids):
        result = []

        for slave_id in slave_ids:
            slave_values = self.read_slave(slave_id)
            result.append(slave_values)

        return result

    def read_slave(self, slave_id):
        try:
            response = self.client.read_holding_registers(
                address=Config.FIRST_REGISTER_ADDRESS,
                count=Config.LAST_REGISTER_ADDRESS - Config.FIRST_REGISTER_ADDRESS + 1,
                unit=slave_id)
        except ConnectionException as ex:
            print("ConnectionException: %s" % str(ex))
            sys.exit()
            return
        except ModbusIOException as ex:
            print("ModbusIOException: %s" % str(ex))
            sys.exit()
            return
        return self.__create_slave_reading(slave_id, response)

    def __create_slave_reading(self, slave_id, response):
        if hasattr(response, 'registers'):
            registers = response.registers
            reading = SlaveReading(slave_id, self.time_service.current_milli_time(), *registers)
        else:
            reading = SlaveReading(slave_id, self.time_service.current_milli_time(), -1, -1, -1, -1)
        return reading
