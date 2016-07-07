from modbus_serial_async import AsyncModbusSerialClient
import tornado.ioloop
from data import Reader, MODBUS_CLIENT_KWARGS

class AsyncReader(Reader):
	def __init__(self):
		super().__init__()

	def on_slave_read(self, async_response, slave_id):
		__on_slave_read = super().on_slave_read
		async_response.addCallback(lambda response: __on_slave_read(response, slave_id))

	def handle_response(self, response, slave_id):
		super().handle_response(response, slave_id)
		if self.should_continue(): self.read_all_slaves()
		else: tornado.ioloop.IOLoop.instance().stop()

	def start_loop(self):
		self.read_all_slaves()
		tornado.ioloop.IOLoop.instance().start()

	def create_client(self):
		self.client = AsyncModbusSerialClient(**MODBUS_CLIENT_KWARGS)