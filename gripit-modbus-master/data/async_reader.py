from modbus_serial_async import AsyncModbusSerialClient
import tornado.ioloop
from data import Reader, MODBUS_CLIENT_KWARGS

class AsyncReader(Reader):
	def __init__(self, should_stop_callback):
		super().__init__(should_stop_callback)
		
	def on_slave_read(self, async_response, slave_id):
		__on_slave_read = super().on_slave_read
		async_response.addCallback(lambda response: __on_slave_read(response, slave_id))
			
	def on_reply(self, response, slave_id):		
		super().on_reply(response, slave_id)
		if (self.should_stop_callback()):
			tornado.ioloop.IOLoop.instance().stop()
		else:
			self.read_all_slaves()

	def create_client(self):
		if self.client == None:
			self.client = AsyncModbusSerialClient(**MODBUS_CLIENT_KWARGS)

	def start_loop(self):		
		self.read_all_slaves()
		tornado.ioloop.IOLoop.instance().start()