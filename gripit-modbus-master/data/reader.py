from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.register_read_message import ReadInputRegistersResponse
from logger import Logger

import RPi.GPIO as GPIO
import sys
import time
import threading

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
	def __init__(self):
		self.__is_started = False
		self.__is_started_lock = threading.Lock()
		self.client = None
		self.current_file_name = None
		self.logger = Logger()

	def should_continue(self):
		return self.__is_started

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
			if not self.should_continue():
				break

	def on_slave_read(self, response, slave_id):
		self.handle_response(response, slave_id)

	def handle_response(self, response, slave_id):
		if isinstance(response, ReadInputRegistersResponse):
			self.logger.write(self.current_file_name, response.registers, slave_id)
		else:
			print("ERROR: %s" % str(response))

	def ensure_client_exists(self):
		if self.client == None: self.create_client()

	def start_loop(self):
		while self.should_continue(): self.read_all_slaves()

	def create_client(self):
		raise Exception('not implemented')

	def start(self):
		self.current_file_name = self.logger.create_new_file()
		self.ensure_client_exists()
		with self.__is_started_lock: self.__is_started = True
		threading.Thread(target=self.start_loop).start()
		
	def stop(self):
		with self.__is_started_lock: self.__is_started = False
