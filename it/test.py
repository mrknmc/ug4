import unittest
import math

from count import *
from code import *


class TestSourceCoding(unittest.TestCase):

    def test_unigram(self):
        """Test that unigram distributions work."""
        a = 'abcdabcaba'
        dist = unigram(a)
        self.assertEqual(dist, {
            'a': 0.4,
            'b': 0.3,
            'c': 0.2,
            'd': 0.1,
        })

    def test_bigram(self):
        """Test that bigram distributions work."""
        a = ' abcdabcaba'
        dist = bigram(a)
        self.assertEqual(dist, {
            ('a', 'b'): 0.3,
            ('b', 'c'): 0.2,
            ('c', 'd'): 0.1,
            (' ', 'a'): 0.1,
            ('d', 'a'): 0.1,
            ('c', 'a'): 0.1,
            ('b', 'a'): 0.1,
        })

    def test_iid_length(self):
        """Test that i.i.d. length is reported correctly."""
        a = 'abcdabcaba'
        dist = unigram(a)
        iid_len = iid_length(a, dist)
        self.assertEqual(iid_len, 21)

    def test_bi_length(self):
        """Test that bigram length is reported correctly."""
        a = ' abcdabcaba'
        uni_dist = unigram(a)
        bi_dist = bigram(a)
        bi_len = bi_length(a, uni_dist, bi_dist)
        self.assertEqual(bi_len, 11)

    def test_round_dist(self):
        """Test rounding and renormalizing a distribution works."""
        a = 'abcdabcaba'
        dist = unigram(a)
        self.assertEqual(round_dist(dist), {
            'a': 103 / 258.,
            'b': 77 / 258.,
            'c': 52 / 258.,
            'd': 26 / 258.,
        })

    def test_iid_round_length(self):
        """Test rounding scheme using i.i.d. works."""
        a = 'abcdabcaba'
        dist = unigram(a)
        self.assertEqual(iid_round_length(a, dist), {
            'header': 216,  # 27 chars, 8 bits each
            'data': 21,
            'total': 237,
        })

    # def test_bi_round_length(self):
    #     """Test rounding scheme using bigrams works."""
    #     a = ' abcdabcaba'
    #     uni_dist = unigram(a)
    #     bi_dist = bigram(a)
    #     self.assertEqual(bi_round_length(a, uni_dist, bi_dist), {
    #         'header': 26 * 8,  # 5x5 chars + first char, 8 bits each
    #         'data': 11,
    #         'total': 211,
    #     })


class MockStdIn(object):
    """"""

    def __init__(self, string):
        self.string = string + '\n'

    def read(self, n):
        ret = self.string[0]
        self.string = self.string[1:]
        return ret


class TestNoisyChannel(unittest.TestCase):

    def test_nutritious_snacks(self):
        """"""
        result = nutritious_snacks('abcd', [97, 2, 6, 21])
        self.assertEqual(result, '\x00`eq')

    def test_encode(self):
        """Test that encoding works correctly."""
        stream = MockStdIn('0100111001010011')
        result = ''.join(encode(stream))
        self.assertEqual(result, '010011110101010001101100')

    def test_decode_no_error(self):
        """Test that code without errors gets decoded correctly."""
        stream = MockStdIn('010011110101010001101100')
        result = ''.join(decode(stream))
        self.assertEqual(result, '0100111001010011')

    def test_decode_one_error(self):
        """Test that code with one error gets decoded correctly."""
        stream = MockStdIn('010111110101010001101100')
        result = ''.join(decode(stream))
        self.assertEqual(result, '0100111001010011')

    def test_parity_bit_one_error(self):
        """Test that code with one parity bit error gets decoded correctly."""
        stream = MockStdIn('010011110101010001101000')
        result = ''.join(decode(stream))
        self.assertEqual(result, '0100111001010011')

    def test_decode_two_errors_raises(self):
        """Test that code with two errors raises Exception."""
        stream = MockStdIn('010111110101010101101100')
        with self.assertRaises(Exception):
            ''.join(decode(stream))

if __name__ == '__main__':
    unittest.main()
