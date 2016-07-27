from gripit.config import Config
from gripit.core.singleton import Singleton
from pymodbus.client.sync import ModbusSerialClient as ModbusClient


class GripitModbusClient(ModbusClient, metaclass=Singleton):
    def __init__(self):
        super().__init__(**Config.MODBUS_CLIENT_KWARGS)
