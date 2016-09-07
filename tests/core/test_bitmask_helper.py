import unittest

from gripit.core.bitmask_helper import BitmaskHelper

class TestBitmaskHelper(unittest.TestCase):
    def test_get_words_with_a_32bit_value_returns_2_words(self):
        words = BitmaskHelper.get_words(int('11111111111110111110011001101001', 2))

        self.assertEqual(words[0], int('1111111111111011', 2))
        self.assertEqual(words[1], int('1110011001101001', 2))

    def test_get_words_with_a_48bit_value_returns_3_words(self):
        words = BitmaskHelper.get_words(int('111111111111101111100110011010011111111111111011', 2))

        self.assertEqual(words[0], int('1111111111111011', 2))
        self.assertEqual(words[1], int('1110011001101001', 2))
        self.assertEqual(words[2], int('1111111111111011', 2))
