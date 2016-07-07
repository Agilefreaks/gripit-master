from modbus_serial_async import AsyncModbusSerialClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.register_read_message import ReadInputRegistersResponse
from pymodbus.client.sync import ModbusSerialClient  as ModbusClient

import logger
import RPi.GPIO as GPIO
import sys
import tornado.ioloop
import time

FIRST_SLAVE_ADDRESS = 2
LAST_SLAVE_ADDRESS = 2

FIRST_REGISTER_ADDRESS = 1;
LAST_REGISTER_ADDRESS = 4;

MODBUS_CLIENT_KWARGS = {
	"method": "rtu",
	"stopbits": 1,
	"bytesize": 8,
	"parity": "N",
	"baudrate": 115200,
	"port": "/dev/ttyAMA0"
}

client = None
current_file_name = None

def read_slave_registers(slave_id):
	global client
	return client.read_input_registers(
		address=FIRST_REGISTER_ADDRESS,
		count=LAST_REGISTER_ADDRESS,
		unit=slave_id
	)

def read_all_slaves(on_slave_read, should_stop_callback):
	for slave_id in range(FIRST_SLAVE_ADDRESS, LAST_SLAVE_ADDRESS + 1):
		try:
			response = read_slave_registers(slave_id)
		except ConnectionException as ex:
			print("ConnectionException: %s" % str(ex))
			sys.exit()
		except ModbusIOException as ex:
			print("ModbusIOException: %s" % str(ex))
			sys.exit()
		on_slave_read(response, slave_id)
		if should_stop_callback():
			break

def handle_response(response, slave_id):
	global current_file_name
	if isinstance(response, ReadInputRegistersResponse):
		logger.write(current_file_name, response.registers, slave_id)
	else:
		print("ERROR: %s" % str(response))

def handle_async_response(async_response, slave_id, should_stop_callback):
	async_response.addCallback(lambda response: on_async_reply(response, slave_id, should_stop_callback)
		
def read_async(should_stop_callback):
	handle_slave_read = lambda async_response, slave_id: handle_async_response(async_response, slave_id, should_stop_callback))
	read_all_slaves(handle_slave_read, should_stop_callback)

def continue_or_stop(should_stop_callback)
	if (should_stop_callback()):
		tornado.ioloop.IOLoop.instance().stop()
	else:
		read_async(should_stop_callback)

def on_async_reply(response, slave_id, should_stop_callback):
	handle_response(response, slave_id)
	continue_or_stop(should_stop_callback)

def start_async_loop(should_stop_callback):
	global client
	client = AsyncModbusSerialClient(**MODBUS_CLIENT_KWARGS)
	read_async(should_stop_callback)
	tornado.ioloop.IOLoop.instance().start()

def on_sync_reply(response, slave_id)
	handle_response(response, slave_id)
	
def read_sync(should_stop_callback)
	handle_slave_read = lambda sync_response, slave_id: on_sync_reply(sync_response, slave_id)
	while not should_stop_callback():
		read_all_slaves(handle_slave_read, should_stop_callback)
		
def start_sync_loop(should_stop_callback):
	global client
	client = ModbusClient(**MODBUS_CLIENT_KWARGS)
	client.connect()	
	read_sync(should_stop_callback)
		
def start(should_stop_callback):
	global current_file_name
	current_file_name = logger.create_new_file()
	start_sync_loop(should_stop_callback)
