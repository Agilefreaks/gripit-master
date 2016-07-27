from gripit.config import Config
from gripit.jobs.job import Job
from gripit.services.gripit_modbus_client import GripitModbusClient


class AddressAutoAssignmentJob(Job):
    def __init__(self):
        self.client = GripitModbusClient()
        self.__assigned_ids = list()
        self.__coils = None
        self.__is_run = False

    def run(self):
        print('Calibration - START !')
        self.__is_run = True
        self.client.connect()
        self.__put_slaves_in_address_assignment_mode()

        while self.is_running():
            self.__check_slave_ids()

    def is_running(self):
        return self.__is_run

    def stop(self):
        self.__is_run = False
        self.client.close()
        print('Calibration - STOP !')

    def __is_used(self, slave_id):
        if slave_id in self.__assigned_ids:
            return 1
        return 0

    def __check_slave_ids(self):
        if Config.NUMBER_OF_SLAVES_ON_BUS == len(self.__assigned_ids):
            self.stop()
            print("Calibration - SUCCESS !")
            return
        self.__read_slave_ids()
        self.__get_unassigned_ids()
        self.__write_unassigned_ids()

    def __get_unassigned_ids(self):
        self.__coils = list()
        for slave_id in range(Config.MIN_SLAVE_ADDRESS, Config.MAX_SLAVE_ADDRESS + 1):
            if self.__is_used(slave_id):
                self.__coils.append(1)
            else:
                self.__coils.append(0)

    def __write_unassigned_ids(self):
        reversed_coils = list(reversed(self.__coils))
        a, b = self.__split_coils(reversed_coils)
        for slave_id in range(Config.MIN_SLAVE_ADDRESS, Config.MAX_SLAVE_ADDRESS + 1):
            self.__write_slave_register(slave_id, Config.CONFIG_REGISTER_254, int(''.join(map(str, a))))
            self.__write_slave_register(slave_id, Config.CONFIG_REGISTER_255, int(''.join(map(str, b))))
            self.__regenerate_slave_id(slave_id)

    def __regenerate_slave_id(self, slave_id):
        if not self.__is_used(slave_id):
            self.__write_slave_register(slave_id,
                                        Config.FORCE_GENERATE_ID_REGISTER_ADDRESS,
                                        1)

    def __put_slaves_in_address_assignment_mode(self):
        for slave_id in range(Config.MIN_SLAVE_ADDRESS, Config.MAX_SLAVE_ADDRESS + 1):
            self.__put_slave_in_address_assignment_mode(slave_id)

    def __put_slave_in_address_assignment_mode(self, slave_id):
        self.__write_slave_register(slave_id,
                                    Config.AUTO_ASSIGNMENT_MODE_REGISTER_ADDRESS,
                                    Config.AUTO_ASSIGNMENT_MODE_ON)

    def __remove_slave_from_address_assignment_mode(self, slave_id):
        self.__write_slave_register(slave_id,
                                    Config.AUTO_ASSIGNMENT_MODE_REGISTER_ADDRESS,
                                    Config.AUTO_ASSIGNMENT_MODE_OFF)

    def __write_slave_register(self, slave_id, register_address, message):
        return self.client.write_register(register_address,
                                          message,
                                          unit=slave_id)

    def __read_slave_ids(self):
        for slave_id in range(Config.MIN_SLAVE_ADDRESS, Config.MAX_SLAVE_ADDRESS + 1):
            self.__read_slave_id(slave_id)

    def __read_slave_id(self, slave_id):
        assigned_id = None
        read_response = self.client.read_holding_registers(
                address=Config.SLAVE_ID_REGISTER_ADDRESS,
                count=1,
                unit=slave_id)
        if hasattr(read_response, 'registers'):
            assigned_id = int(read_response.registers[0])
            self.__remove_slave_from_address_assignment_mode(assigned_id)
            self.__save_assigned_id(assigned_id)
        return assigned_id

    def __save_assigned_id(self, assigned_id):
        if assigned_id not in self.__assigned_ids:
            self.__assigned_ids.append(assigned_id)

    def __split_coils(self, list):
        half = len(list)//2
        return list[:half], list[half:]
