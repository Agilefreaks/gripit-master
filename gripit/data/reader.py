from pymodbus.exceptions import ConnectionException, ModbusIOException
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import pymodbus.device as Device

from .logger import Logger
from gripit.setup import Setup

import sys
import time
import threading


class Reader:
    MODBUS_CLIENT = ModbusClient(**Setup.MODBUS_CLIENT_KWARGS)

    def __init__(self):
        self._is_started = False
        self._is_started_lock = threading.Lock()
        self.client = None
        self.current_file_name = None
        self.logger = Logger()

    def should_continue(self):
        return self._is_started

    def read_input_registers(self, slave_id):
        return self.client.read_input_registers(
            address=Setup.FIRST_REGISTER_ADDRESS,
            count=Setup.LAST_REGISTER_ADDRESS,
            unit=slave_id)

    def read_slave_registers(self, slave_id):
        try:
            response = self.read_input_registers(slave_id)
        except ConnectionException as ex:
            print("ConnectionException: %s" % str(ex))
            sys.exit()
        except ModbusIOException as ex:
            print("ModbusIOException: %s" % str(ex))
            sys.exit()
        return response

    def read_all_slaves(self):
        for slave_id in range(Setup.FIRST_SLAVE_ADDRESS,
                              Setup.LAST_SLAVE_ADDRESS + 1):
            response = self.read_slave_registers(slave_id)
            self.handle_response(response, slave_id)
            if not self.should_continue():
                break

    def handle_response(self, response, slave_id):
        if hasattr(response, 'registers'):
            self.write_registers(response.registers, slave_id)
        else:
            self.write_registers([-1, -1, -1, -1], slave_id)

    def write_registers(self, registers, slave_id):
        return self.logger.write(self.current_file_name,
                                 registers,
                                 slave_id)

    def ensure_client_exists(self):
        if self.client is None:
            self.create_client(self.MODBUS_CLIENT)

    def start_loop(self):
        while self.should_continue():
            self.read_all_slaves()

    def create_client(self, client):
        self.client = client
        self.client.connect()

    def start(self):
        self.current_file_name = self.logger.create_new_file()
        self.ensure_client_exists()
        with self._is_started_lock:
            self._is_started = True
        threading.Thread(target=self.start_loop).start()

    def stop(self):
        with self._is_started_lock:
            self._is_started = False
