import unittest
import os
import shutil

from gripit.data.logger import Logger
from mock import patch, Mock


class TestLogger(unittest.TestCase):
    def setUp(self):
        self.logger = Logger()
        current_milli_time_spy = Mock()
        current_milli_time_spy.return_value = str(45234543)
        self.logger.current_milli_time = current_milli_time_spy

    def test_create_directory(self):
        self.assertEqual(os.path.exists(self.logger.PATH), True)

    def test_create_new_file(self):
        self.assertEqual(self.logger.create_new_file(), str(45234543)+'.csv')

    # def test_write(self):
    #     file_name = self.logger.create_new_file()
    #     result = 'registers'
    #     hold_id = '1'
    #     self.logger.write(file_name, result, hold_id)
    #     self.assertEqual(['1', str(45234543)] + 'registers')
