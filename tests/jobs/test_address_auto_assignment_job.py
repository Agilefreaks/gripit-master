import unittest
import time

from mock import patch, PropertyMock
from threading import Thread

from pymodbus.register_read_message import ReadHoldingRegistersResponse

from gripit.config import Config
from gripit.jobs.address_auto_assignment_job import AddressAutoAssignmentJob


class TestAddressAutoAssignmentJob(unittest.TestCase):
    MOCK_MIN_ADDRESS = 1
    MOCK_MAX_ADDRESS = 4

    @patch('gripit.jobs.address_auto_assignment_job.GripitModbusClient', autospec=True)
    def setUp(self, MockModbusClient):
        min_patcher = patch.object(Config, 'MIN_SLAVE_ADDRESS', new_callable=PropertyMock,
                                   return_value=self.MOCK_MIN_ADDRESS)
        max_patcher = patch.object(Config, 'MAX_SLAVE_ADDRESS', new_callable=PropertyMock,
                                   return_value=self.MOCK_MAX_ADDRESS)
        self.mock_min_slave_address = min_patcher.start()
        self.mock_max_slave_address = max_patcher.start()
        self.addCleanup(min_patcher.stop)
        self.addCleanup(max_patcher.stop)

        self.mock_client = MockModbusClient()

        self.job = AddressAutoAssignmentJob()

    def test_run_will_connect_to_modbus_client(self):
        self.__run_job()

        self.mock_client.connect.assert_called()

    def test_run_will_write_to_the_auto_assignment_register_with_the_on_word_for_all_slave_addresses(self):
        self.__run_job()

        for slave_id in range(self.MOCK_MIN_ADDRESS, self.MOCK_MAX_ADDRESS + 1):
            self.mock_client.write_register.assert_any_call(Config.AUTO_ASSIGNMENT_MODE_REGISTER_ADDRESS,
                                                            Config.AUTO_ASSIGNMENT_MODE_ON,
                                                            unit=slave_id)

    def test_run_will_read_from_the_slave_id_register_for_all_slave_addresses(self):
        self.__run_job()

        for slave_id in range(self.MOCK_MIN_ADDRESS, self.MOCK_MAX_ADDRESS + 1):
            self.mock_client.read_holding_registers.assert_any_call(address=Config.SLAVE_ID_REGISTER_ADDRESS,
                                                                    count=1,
                                                                    unit=slave_id)

    def test_run_will_stop_calibration_mode_for_all_valid_responses(self):
        existing_slave_id = 5
        self.mock_client.read_holding_registers.return_value = ReadHoldingRegistersResponse('%d' % existing_slave_id)

        self.__run_job()

        self.mock_client.write_register.assert_any_call(Config.AUTO_ASSIGNMENT_MODE_REGISTER_ADDRESS,
                                                        Config.AUTO_ASSIGNMENT_MODE_OFF,
                                                        unit=existing_slave_id)

    def test_run_will_map_all_ids_in_two_16_bits_int_values_and_write_them_to_config_registers(self):
        assigned_id = 2

        self.mock_client.read_holding_registers.return_value = ReadHoldingRegistersResponse('%d' % assigned_id)

        self.__run_job()

        ids_3217 = int('000000000000000')
        self.mock_client.write_register.assert_any_call(Config.CONFIG_REGISTER_254,
                                                        ids_3217,
                                                        unit=assigned_id)

        ids_1601 = int('000000000000010')
        self.mock_client.write_register.assert_any_call(Config.CONFIG_REGISTER_255,
                                                        ids_1601,
                                                        unit=assigned_id)

    def test_run_will_force_all_slaves_with_unassigned_addresses_to_generate_new_address(self):
        assigned_id = 3
        self.mock_client.read_holding_registers.return_value = ReadHoldingRegistersResponse('%d' % assigned_id)

        self.__run_job()

        for slave_id in range(self.MOCK_MIN_ADDRESS, self.MOCK_MAX_ADDRESS + 1):
            if slave_id is not assigned_id:
                self.mock_client.write_register.assert_any_call(Config.FORCE_GENERATE_ID_REGISTER_ADDRESS,
                                                                1,
                                                                unit=slave_id)

    def test_run_will_stop_auto_assignment_if_all_slaves_have_valid_addresses(self):
        number_of_slaves_on_bus = 3
        with patch.object(Config, 'NUMBER_OF_SLAVES_ON_BUS', new_callable=PropertyMock, return_value=number_of_slaves_on_bus):
            for slave_id in range(1, number_of_slaves_on_bus + 1):
                self.mock_client.read_holding_registers.return_value = ReadHoldingRegistersResponse('%d' % slave_id)
                self.__run_job_without_stop()

        self.mock_client.close.assert_called()

    def test_is_running_will_return_false_if_job_dont_run(self):
        subject = self.job.is_running()

        self.assertFalse(subject)

    def test_stop_will_close_connection_to_modbus_client(self):
        self.job.stop()

        self.mock_client.close.assert_called()

    def __run_job(self):
        thread = Thread(target=self.job.run)
        thread.start()
        time.sleep(0.1)
        self.job.stop()

    def __run_job_without_stop(self):
        thread = Thread(target=self.job.run)
        thread.start()
        time.sleep(0.1)
