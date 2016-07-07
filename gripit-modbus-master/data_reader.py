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

REGISTERS_FIRST_ADDRESS = 1;
REGISTERS_LAST_ADDRESS = 4;

client = None
current_file_name = None
kwargs = {
	"method": "rtu",
	"stopbits": 1,
	"bytesize": 8,
	"parity": "N",
	"baudrate": 115200,
	"port": "/dev/ttyAMA0"
}

current_milli_time = lambda: int(round(time.time() * 1000))

def read_slave_registers(slave_id):
	return client.read_input_registers(
		address=REGISTERS_FIRST_ADDRESS,
		count=REGISTERS_LAST_ADDRESS,
		unit=slave_id
	)

def read_async(should_stop_callback):
	global client
	for slave_id in range(FIRST_SLAVE_ADDRESS, LAST_SLAVE_ADDRESS + 1):
		try:
			res = read_slave_registers(slave_id)
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
		logger.write(current_file_name, result.registers, slave_id)
	else:
		print("ERROR: %s" % str(result))
	if (should_stop_callback()):
		tornado.ioloop.IOLoop.instance().stop()
	else:
		read_async(should_stop_callback)

def start_async_loop(should_stop_callback):
	global client
	global kwargs

	client = AsyncModbusSerialClient(**kwargs)	
	read_async(should_stop_callback)
	tornado.ioloop.IOLoop.instance().start()

def start_sync_loop(should_stop_callback):
	global client	
	global current_file_name
	global kwargs

	client = ModbusClient(**kwargs)
	client.connect()
	should_stop = should_stop_callback()
	while not should_stop:
		for slave_id in range(FIRST_SLAVE_ADDRESS, LAST_SLAVE_ADDRESS + 1):
			result = read_slave_registers(slave_id)
			logger.write(current_file_name, result.registers, slave_id)
			should_stop = should_stop_callback()
			if not should_stop:
				break

def start(should_stop_callback):
	global current_file_name
	current_file_name = str(current_milli_time()) + '.csv'
	logger.create(current_file_name)
	start_sync_loop(should_stop_callback)
