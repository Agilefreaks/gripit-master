from pymodbus.client.sync import ModbusSerialClient  as ModbusClient
from data import Reader, MODBUS_CLIENT_KWARGS

class SyncReader(Reader):
	def __init__(self):
		super().__init__()

	def create_client(self):
		self.client = ModbusClient(**MODBUS_CLIENT_KWARGS)
		self.client.connect()
