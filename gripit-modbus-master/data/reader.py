from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.register_read_message import ReadInputRegistersResponse
from logger import Logger

import RPi.GPIO as GPIO
import sys
import time

FIRST_SLAVE_ADDRESS = 2
LAST_SLAVE_ADDRESS = 2

FIRST_REGISTER_ADDRESS = 1
LAST_REGISTER_ADDRESS = 4

MODBUS_CLIENT_KWARGS = {
	"method": "rtu",
	"stopbits": 1,
	"bytesize": 8,
	"parity": "N",
	"baudrate": 115200,
	"port": "/dev/ttyAMA0"
}

class Reader:
	def __init__(self, should_stop_callback):
		self.client = None
		self.current_file_name = None
		self.should_stop_callback = should_stop_callback
		self.logger = Logger()

	def should_stop(self):
		return self.should_stop_callback()
		
	def read_slave_registers(self, slave_id):
		return self.client.read_input_registers(
			address=FIRST_REGISTER_ADDRESS,
			count=LAST_REGISTER_ADDRESS,
			unit=slave_id
		)

	def read_all_slaves(self):
		for slave_id in range(FIRST_SLAVE_ADDRESS, LAST_SLAVE_ADDRESS + 1):
			try:
				response = self.read_slave_registers(slave_id)
			except ConnectionException as ex:
				print("ConnectionException: %s" % str(ex))
				sys.exit()
			except ModbusIOException as ex:
				print("ModbusIOException: %s" % str(ex))
				sys.exit()
			self.on_slave_read(response, slave_id)
			if self.should_stop_callback():
				break

	def handle_response(self, response, slave_id):
		if isinstance(response, ReadInputRegistersResponse):
			self.logger.write(self.current_file_name, response.registers, slave_id)
		else:
			print("ERROR: %s" % str(response))

	def on_reply(self, response, slave_id):
		self.handle_response(response, slave_id)
			
	def on_slave_read(self, response, slave_id):
		self.on_reply(response, slave_id)

	def ensure_client_exists(self):
		if self.client == None:
			self.create_client()
			
	def create_client(self):
		raise Exception('not implemented')
		
	def start_loop(self):
		raise Exception('not implemented')
			
	def start(self):
		self.current_file_name = self.logger.create_new_file()
		self.ensure_client_exists()
		self.start_loop()
