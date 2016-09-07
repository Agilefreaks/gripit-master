from gripit.config import Config
from gripit.jobs.job import Job
from gripit.services.gripit_modbus_client import GripitModbusClient
from gripit.core.id_map import IdMap
from gripit.core.bitmask_helper import BitmaskHelper


class AddressAutoAssignmentJob(Job):
    def __init__(self):
        self.client = GripitModbusClient()
        self.__id_map = IdMap(Config.MIN_SLAVE_ADDRESS, Config.MAX_SLAVE_ADDRESS)
        self.__is_running = False

    def run(self):
        print('Calibration - START !')
        self.__is_running = True
        self.client.connect()
        self.__put_slaves_in_address_assignment_mode()
        while self.is_running():
            if self.__discovered_all_slaves():
                print("Calibration - SUCCESS !")
                self.stop()
            else:
                self.__update_slave_ids()

    def is_running(self):
        return self.__is_running

    def stop(self):
        self.__is_running = False
        self.client.close()
        print('Calibration - STOP !')

    def __put_slaves_in_address_assignment_mode(self):
        self.__write_to_slaves(self.__id_map.all_ids,
                               Config.AUTO_ASSIGNMENT_MODE_REGISTER_ADDRESS,
                               Config.AUTO_ASSIGNMENT_MODE_ON)

    def __update_slave_ids(self):
        discovered_ids = self.__discover_assigned_ids()
        self.__id_map.set_as_assigned(discovered_ids)
        self.__remove_slaves_from_address_assignment_mode(discovered_ids)
        self.__write_unassigned_ids()
        self.__regenerate_slave_ids()

    def __discover_assigned_ids(self):
        discovered_ids = list()
        for slave_id in self.__id_map.unassigned_ids:
            read_response = self.client.read_holding_registers(
                address=Config.SLAVE_ID_REGISTER_ADDRESS,
                count=1,
                unit=slave_id)
            if hasattr(read_response, 'registers'):
                discovered_ids.append(slave_id)
        return discovered_ids

    def __remove_slaves_from_address_assignment_mode(self, slave_ids):
        self.__write_to_slaves(slave_ids,
                               Config.AUTO_ASSIGNMENT_MODE_REGISTER_ADDRESS,
                               Config.AUTO_ASSIGNMENT_MODE_OFF)

    def __write_unassigned_ids(self):
        ids_bitmask = self.__id_map.to_bit_mask()
        words = BitmaskHelper.get_words(ids_bitmask)
        for index, word in enumerate(reversed(words)):
            self.__write_to_slaves(self.__id_map.unassigned_ids, Config.MAX_REGISTER_ADDRESS - index, word)

    def __regenerate_slave_ids(self):
        self.__write_to_slaves(self.__id_map.unassigned_ids,
                               Config.FORCE_GENERATE_ID_REGISTER_ADDRESS,
                               Config.REGENERATE_ID_COMMAND)

    def __write_to_slaves(self, slave_ids, register_address, value):
        for slave_id in slave_ids:
            self.client.write_register(register_address, value, unit=slave_id)

    def __discovered_all_slaves(self):
        # print(len(self.__id_map.assigned_ids))
        # print(self.__id_map.assigned_ids)
        # print(Config.NUMBER_OF_SLAVES_ON_BUS)
        return len(self.__id_map.assigned_ids) > Config.NUMBER_OF_SLAVES_ON_BUS
