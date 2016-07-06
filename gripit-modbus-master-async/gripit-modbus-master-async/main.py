from async_rtu import AsyncModbusSerialClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.register_read_message import ReadInputRegistersResponse

import file
import RPi.GPIO as GPIO
import sys
import tornado.ioloop

FIRST_SLAVE_ADDRESS = 2
LAST_SLAVE_ADDRESS = 2

client = AsyncModbusSerialClient(
	method='rtu',
	stopbits=1,
	bytesize=8,
	parity='N',
	baudrate=115200,
	port='/dev/ttyAMA0'
)

def read_async(should_stop_callback):
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

def async_reply(result, unit, should_stop_callback):
	if isinstance(result, ReadInputRegistersResponse):
		file.write('result.csv', result.registers, unit)
		print(result.registers)
	else:
		print("ERROR: %s" % str(result))
	if (not should_stop_callback()):
		read_async(should_stop_callback)
	else:
		tornado.ioloop.IOLoop.instance().stop()

def start(should_stop_callback):
	file.create('result.csv')
	read_async(should_stop_callback)
	tornado.ioloop.IOLoop.instance().start()