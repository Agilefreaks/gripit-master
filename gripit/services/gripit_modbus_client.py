import time

from gripit.config import Config
from gripit.core.singleton import Singleton
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


class GripitModbusClient(ModbusClient, metaclass=Singleton):
    def __init__(self):
        super().__init__(**Config.MODBUS_CLIENT_KWARGS)

    def read_holding_registers(self, address, count=1, **kwargs):
        response = super().read_holding_registers(address=address, count=count, **kwargs)
        time.sleep(Config.reading_sleep_time)
        return response
