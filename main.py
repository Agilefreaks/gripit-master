from time import time

import pymodbus
from pymodbus.client.sync import ModbusSerialClient as ModbusClient

client = ModbusClient(
	method='rtu', 
	port='/dev/ttyAMA0',
	stopbits=1,
	bytesize=8,
	parity='N',
	baudrate=19200,
        timeout=0.03
)

rtu = client.connect()
print "Connection: %s" % rtu
start = time()
for index in range(0, 1000):
	rr = client.read_input_registers(1, 4, unit=0x01)
	print "Result = %s" % rr
	print (rr.registers)
end = time()
print end-start
client.close()
