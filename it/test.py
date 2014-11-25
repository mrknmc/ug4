import unittest

from itertools import chain, combinations
from count import *
from flipper import *
from code import *


def generate_num(n):
    """Generates a random n-bit binary number."""
    pow2 = pow(2, n)
    return bin(int(round(random.random() * pow2))).lstrip('0b').zfill(n)


class MockStdIn(object):
    """Mock of stdin to test Encoder and Decoder."""

    def __init__(self, string):
        self.string = string + '\n'

    def read(self, n):
        ret = self.string[0]
        self.string = self.string[1:]
        return ret


class TestSourceCoding(unittest.TestCase):

    """Tests related to first part of the assignment."""

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
        self.assertEqual(norm_dist(round_dist(dist)), {
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

    def test_bi_round_length(self):
        """Test rounding scheme using bigrams works."""
        a = ' abcdabcaba'
        uni_dist = unigram(a)
        bi_dist = bigram(a)
        self.assertEqual(bi_round_length(a, uni_dist, bi_dist), {
            'header': 6048,  # 27 * 27 + 27 chars, 8 bits each
            'data': 11,
            'total': 6059,
        })


class TestNoisyChannel(unittest.TestCase):

    """Tests related to the second part of the assignment."""

    def test_nutritious_snacks(self):
        """Test nutritious_snacks function."""
        result = nutritious_snacks('abcd', [97, 2, 6, 21])
        self.assertEqual(result, '\x00`eq')

    def test_encode(self):
        """Test that encoding works correctly."""
        stream = MockStdIn('0100')
        result = ''.join(encode(stream))
        self.assertEqual(result, '01100001')

    def test_decode_no_error(self):
        """Test that code without errors gets decoded correctly."""
        stream = MockStdIn('01100001')
        result = ''.join(decode(stream))
        self.assertEqual(result, '0100')

    def test_decode_one_error(self):
        """Test that code with one error gets decoded correctly."""
        stream = MockStdIn('01110001')
        result = ''.join(decode(stream))
        self.assertEqual(result, '0100')

    def test_parity_bit_one_error(self):
        """Test that code with one parity bit error gets decoded correctly."""
        stream = MockStdIn('01100101')
        result = ''.join(decode(stream))
        self.assertEqual(result, '0100')

    def test_decode_two_errors_raises(self):
        """Test that code with two errors returns errors."""
        stream = MockStdIn('11110001')
        result = ''.join(decode(stream))
        self.assertEqual(result, '1110')


class TestBitError(unittest.TestCase):

    """Tests verifying that bit error computed analytically matches."""

    def analytic_bit_error(self, f, k):
        """Counts the average number of bit errors in k transmissions."""
        failure = 0.
        total = 0
        for i in range(k):
            number = generate_num(4)
            stream = MockStdIn(number)
            encoded = ''.join(encode(stream))
            noised = ''.join(noise(MockStdIn(encoded), f=f))
            decoded = ''.join(decode(MockStdIn(noised)))
            total += len(number)
            for enc, dec in zip(number, decoded):
                if enc != dec:
                    failure += 1
        return failure / total

    def real_bit_error(self, f):
        """Computes probability of bit error."""
        total_failure = 0.
        number = generate_num(4)
        stream = MockStdIn(number)
        encoded = ''.join(encode(stream))
        enc_len = len(encoded)
        flippy = chain(*(combinations(range(8), i) for i in range(enc_len + 1)))

        for flip in flippy:
            copy = [int(c) for c in encoded]
            prob = pow(f, len(flip)) * pow(1 - f, 8 - len(flip))
            for pos in flip:
                copy[pos] = 1 - copy[pos]  # flip it
            noised = ''.join(str(c) for c in copy)
            decoded = ''.join(decode(MockStdIn(noised)))
            failure = 0.
            for enc, dec in zip(number, decoded):
                if enc != dec:
                    failure += 1
            total_failure += prob * (failure / 4)
        return total_failure

    def analytic_bit_error_test_04(self):
        """Test with 0.4 probability."""
        real_failure_rate = self.real_bit_error(0.4)
        failure_rate = self.analytic_bit_error(0.4, 10000)
        self.assertAlmostEqual(real_failure_rate, failure_rate, places=1)

    def analytic_bit_error_test_01(self):
        """Test with 0.1 probability."""
        real_failure_rate = self.real_bit_error(0.1)
        failure_rate = self.analytic_bit_error(0.1, 10000)
        self.assertAlmostEqual(real_failure_rate, failure_rate, places=2)

    def analytic_bit_error_test_0001(self):
        """Test with 0.001 probability."""
        real_failure_rate = self.real_bit_error(0.001)
        failure_rate = self.analytic_bit_error(0.001, 100000)
        self.assertAlmostEqual(real_failure_rate, failure_rate, places=5)


if __name__ == '__main__':
    unittest.main()
