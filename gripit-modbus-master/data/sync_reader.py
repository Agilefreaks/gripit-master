from pymodbus.client.sync import ModbusSerialClient  as ModbusClient
from data import Reader, MODBUS_CLIENT_KWARGS

class SyncReader(Reader):
	def __init__(self, should_stop_callback):		
		super().__init__(should_stop_callback)

	def create_client(self):
		self.client = ModbusClient(**MODBUS_CLIENT_KWARGS)
		self.client.connect()
		
	def start_loop(self):		
		while not self.should_stop():
			self.read_all_slaves()