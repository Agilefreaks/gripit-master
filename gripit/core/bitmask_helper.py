import math


class BitmaskHelper:
    WORD_LENGTH = 16

    @staticmethod
    def get_words(bitmask):
        words = list()
        bit_length = bitmask.bit_length()
        words_count = math.ceil(bit_length / BitmaskHelper.WORD_LENGTH)
        for index in range(0, words_count):
            words.append((bitmask >> BitmaskHelper.WORD_LENGTH * index) & 0xffff)

        return list(reversed(words))
