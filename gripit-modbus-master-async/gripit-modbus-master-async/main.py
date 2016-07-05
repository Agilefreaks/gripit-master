from async_rtu import AsyncModbusSerialClient
from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.register_read_message import ReadInputRegistersResponse
import tornado.ioloop
import sys

from time import time

from file import create
from file import write

client = AsyncModbusSerialClient(
	method='rtu',
	stopbits=1,
	bytesize=8,
	parity='N',
	baudrate=115200,
	port='/dev/ttyAMA0'
)

def read_async(count, start):
	try:
		res = client.read_input_registers(address=1, count=4, unit=2)
	except ConnectionException as ex:
		print("ConnectionException: %s" % str(ex))
		sys.exit()
	except ModbusIOException as ex:
		print("ModbusIOException: %s" % str(ex))
		sys.exit()
	res.addCallback(lambda result: async_reply(result, count, start))

def async_reply(result, count, start):
	if isinstance(result, ReadInputRegistersResponse):
		write('result.csv', result.registers)
		print(result.registers)
	else:
		print("ERROR: %s" % str(result))
	if (count < 10):
		read_async(count + 1, start)
	else:
		end = time()
		print(end-start)
		tornado.ioloop.IOLoop.instance().stop()

def start():
	#Save Start Time
	start = time()
	
	# Create CSV FILE
	create('result.csv')
	
	#Start Reading Registers
	read_async(0, start)
	tornado.ioloop.IOLoop.instance().start()
	
start()
