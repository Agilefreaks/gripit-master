from async_rtu import AsyncModbusSerialClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.register_read_message import ReadInputRegistersResponse
from time import time

from file import create
from file import write

import RPi.GPIO as GPIO
import sys
import tornado.ioloop

client = AsyncModbusSerialClient(
	method='rtu',
	stopbits=1,
	bytesize=8,
	parity='N',
	baudrate=115200,
	port='/dev/ttyAMA0'
)

def read_async(should_stop_callback):
	try:
		res = client.read_input_registers(address=1, count=4, unit=2)
	except ConnectionException as ex:
		print("ConnectionException: %s" % str(ex))
		sys.exit()
	except ModbusIOException as ex:
		print("ModbusIOException: %s" % str(ex))
		sys.exit()
	res.addCallback(lambda result: async_reply(result, should_stop_callback))

def async_reply(result, should_stop_callback):
	if isinstance(result, ReadInputRegistersResponse):
		write('result.csv', result.registers)
		print(result.registers)
	else:
		print("ERROR: %s" % str(result))
	if (not should_stop_callback()):
		read_async(should_stop_callback)
	else:
		tornado.ioloop.IOLoop.instance().stop()

def start(should_stop_callback):
	create('result.csv')
	read_async(should_stop_callback)
	tornado.ioloop.IOLoop.instance().start()