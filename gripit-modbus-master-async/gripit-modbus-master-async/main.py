from async_rtu import AsyncModbusSerialClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.register_read_message import ReadInputRegistersResponse
from pymodbus.client.sync import ModbusSerialClient  as ModbusClient

import file
import RPi.GPIO as GPIO
import sys
import tornado.ioloop
import time

FIRST_SLAVE_ADDRESS = 2
LAST_SLAVE_ADDRESS = 2

client = None
current_file_name = None

current_milli_time = lambda: int(round(time.time() * 1000))

def read_async(should_stop_callback):
	global client
	for slave_id in range(FIRST_SLAVE_ADDRESS, LAST_SLAVE_ADDRESS + 1):
		try:
			res = client.read_input_registers(address=1, count=4, unit=slave_id)
		except ConnectionException as ex:
			print("ConnectionException: %s" % str(ex))
			sys.exit()
		except ModbusIOException as ex:
			print("ModbusIOException: %s" % str(ex))
			sys.exit()
		res.addCallback(lambda result: async_reply(result, slave_id, should_stop_callback))

def async_reply(result, slave_id, should_stop_callback):
	global current_file_name
	if isinstance(result, ReadInputRegistersResponse):
		file.write(current_file_name, result.registers, slave_id)
	else:
		print("ERROR: %s" % str(result))
	if (not should_stop_callback()):
		read_async(should_stop_callback)
	else:
		tornado.ioloop.IOLoop.instance().stop()

def start_async_loop(should_stop_callback):
	global client
	global current_file_name
	file.create(current_file_name)
	client = AsyncModbusSerialClient(
		method='rtu',
		stopbits=1,
		bytesize=8,
		parity='N',
		baudrate=115200,
		port='/dev/ttyAMA0'
	)	
	read_async(should_stop_callback)
	tornado.ioloop.IOLoop.instance().start()
		
def start_sync_loop(should_stop_callback):
	global client
	file.create(current_file_name)	
	client = ModbusClient(
		method='rtu',
		stopbits=1,
		bytesize=8,
		parity='N',
		baudrate=115200,
		port='/dev/ttyAMA0'
	)
	client.connect()
	should_stop = should_stop_callback()
	while not should_stop:
		for slave_id in range(FIRST_SLAVE_ADDRESS, LAST_SLAVE_ADDRESS + 1):
			result = client.read_input_registers(address=1, count=8, unit=slave_id)
			file.write(current_file_name, result.registers, slave_id)
			should_stop = should_stop_callback()
			if not should_stop:
				break
		
def start(should_stop_callback):
	global current_file_name
	current_file_name = str(current_milli_time()) + '.csv'
	start_async_loop(should_stop_callback)
	