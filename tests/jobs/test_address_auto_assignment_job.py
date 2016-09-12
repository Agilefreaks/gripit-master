import unittest
import time

from mock import patch, PropertyMock
from threading import Thread

from pymodbus.register_read_message import ReadHoldingRegistersResponse

from gripit.config import Config
from gripit.jobs.address_auto_assignment_job import AddressAutoAssignmentJob


class TestAddressAutoAssignmentJob(unittest.TestCase):
    MOCK_MIN_ADDRESS = 1
    MOCK_MAX_ADDRESS = 17

    @patch('gripit.jobs.address_auto_assignment_job.GripitModbusClient', autospec=True)
    def setUp(self, MockModbusClient):
        min_patcher = patch.object(Config, 'MIN_SLAVE_ADDRESS', new_callable=PropertyMock,
                                   return_value=self.MOCK_MIN_ADDRESS)
        max_patcher = patch.object(Config, 'MAX_SLAVE_ADDRESS', new_callable=PropertyMock,
                                   return_value=self.MOCK_MAX_ADDRESS)
        slave_count_patcher = patch.object(Config, 'NUMBER_OF_SLAVES_ON_BUS', new_callable=PropertyMock,
                                           return_value=self.MOCK_MAX_ADDRESS - self.MOCK_MIN_ADDRESS + 1)
        self.mock_min_slave_address = min_patcher.start()
        self.mock_max_slave_address = max_patcher.start()
        self.mock_number_of_slaves = slave_count_patcher.start()
        self.addCleanup(min_patcher.stop)
        self.addCleanup(max_patcher.stop)
        self.addCleanup(slave_count_patcher.stop)

        self.mock_client = MockModbusClient()

        self.job = AddressAutoAssignmentJob()

    def test_run_will_connect_to_modbus_client(self):
        self.__run_and_stop_job()

        self.mock_client.connect.assert_called_once()

    def test_run_will_write_to_the_auto_assignment_register_with_the_on_word_for_all_slave_addresses(self):
        self.__run_and_stop_job()

        for slave_id in range(self.MOCK_MIN_ADDRESS, self.MOCK_MAX_ADDRESS + 1):
            self.mock_client.write_register.assert_any_call(Config.AUTO_ASSIGNMENT_MODE_REGISTER_ADDRESS,
                                                            Config.AUTO_ASSIGNMENT_MODE_ON,
                                                            unit=slave_id)

    def test_run_will_read_from_the_slave_id_register_for_all_slave_addresses(self):
        self.__run_and_stop_job()

        for slave_id in range(self.MOCK_MIN_ADDRESS, self.MOCK_MAX_ADDRESS + 1):
            self.mock_client.read_holding_registers.assert_any_call(address=Config.SLAVE_ID_REGISTER_ADDRESS,
                                                                    count=1,
                                                                    unit=slave_id)

    def test_run_will_stop_calibration_mode_for_all_valid_responses(self):
        self.mock_client.read_holding_registers.return_value = ReadHoldingRegistersResponse('0')

        self.__run_and_stop_job()

        for slave_id in range(self.MOCK_MIN_ADDRESS, self.MOCK_MAX_ADDRESS + 1):
            self.mock_client.write_register.assert_any_call(Config.AUTO_ASSIGNMENT_MODE_REGISTER_ADDRESS,
                                                            Config.AUTO_ASSIGNMENT_MODE_OFF,
                                                            unit=slave_id)

    def test_run_some_ids_are_unassigned_will_map_all_id_usages_to_word_values_and_write_them_to_config_registers(self):
        unassigned_id = 2
        self.__setup_unassigned_ids([unassigned_id])

        self.__run_and_stop_job()

        word1 = int('0000000000000001', 2)
        word2 = int('1111111111111101', 2)
        self.mock_client.write_register.assert_any_call(254, word1, unit=unassigned_id)
        self.mock_client.write_register.assert_any_call(255, word2, unit=unassigned_id)

    def test_run_will_force_all_slaves_with_unassigned_addresses_to_generate_new_address(self):
        unassigned_ids = [2, 3]
        self.__setup_unassigned_ids(unassigned_ids)

        self.__run_and_stop_job()

        for slave_id in unassigned_ids:
            self.mock_client.write_register.assert_any_call(Config.FORCE_GENERATE_ID_REGISTER_ADDRESS,
                                                            Config.REGENERATE_ID_COMMAND,
                                                            unit=slave_id)

    def test_run_will_stop_auto_assignment_if_all_slaves_have_valid_addresses(self):
        total_slave_count = 3
        self.mock_number_of_slaves.return_value = total_slave_count
        self.mock_client.read_holding_registers.return_value = ReadHoldingRegistersResponse('0')

        self.__run_job_with_timeout(1)  # wait for the job to finish by itself

        self.mock_client.close.assert_called_once()

    def test_is_running_will_return_false_if_job_was_not_started(self):
        subject = self.job.is_running()

        self.assertFalse(subject)

    def test_is_running_will_return_true_if_job_was_started(self):
        self.__setup_unassigned_ids([2])
        self.__run_job()

        self.assertTrue(self.job.is_running())
        self.job.stop()

    def test_stop_will_close_connection_to_modbus_client(self):
        self.job.stop()

        self.mock_client.close.assert_called()

    def __run_job(self, time_to_wait=0.05):
        thread = Thread(target=self.job.run)
        thread.start()
        time.sleep(time_to_wait)

    def __run_job_with_timeout(self, timeout):
        self.__run_job(0)
        start_time = time.time()
        while self.mock_client.close.call_count == 0:
            if time.time() - start_time > timeout:
                self.job.stop()
                raise Exception("test timed out")
            time.sleep(0.05)

    def __run_and_stop_job(self):
        self.__run_job()
        self.job.stop()

    def __setup_unassigned_ids(self, ids):
        def mock_read_holding_registers(address, count, unit):
            return None if unit in ids else ReadHoldingRegistersResponse('%d' % address)

        self.mock_client.read_holding_registers.side_effect = mock_read_holding_registers
