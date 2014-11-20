import unittest

from count import *
from flipper import *
from code import *


class MockStdIn(object):
    """Mock of stdin to test Encoder and Decoder."""

    def __init__(self, string):
        self.string = string + '\n'

    def read(self, n):
        ret = self.string[0]
        self.string = self.string[1:]
        return ret


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

    def generate_num(self, n):
        """Generates a random n-bit binary number."""
        pow2 = pow(2, n)
        return bin(int(round(random.random() * pow2))).lstrip('0b').zfill(n)

    def block_error(self, f):
        """Counts the number of block errors."""
        success = failure = 0.
        total = 100000
        for i in range(total):
            number = generate_num(4)
            stream = MockStdIn(number)
            encoded = ''.join(encode(stream))
            noised = ''.join(noise(MockStdIn(encoded), f=f))
            decoded = ''.join(decode(MockStdIn(noised)))
            if decoded == number:
                success += 1
            else:
                failure += 1
        return success / total, failure / total

    def bit_error(self, f):
        """Counts the average number of bit errors."""
        success = failure = 0.
        total = 0
        for i in range(100000):
            number = generate_num(4)
            stream = MockStdIn(number)
            encoded = ''.join(encode(stream))
            noised = ''.join(noise(MockStdIn(encoded), f=f))
            decoded = ''.join(decode(MockStdIn(noised)))
            total += len(number)
            for enc, dec in zip(number, decoded):
                if enc == dec:
                    success += 1
                else:
                    failure += 1
        return success / total, failure / total

    def bit_error_prob(self):
        """Computes probability of bit error."""
        total_failure = 0.
        number = generate_num(4)
        stream = MockStdIn(number)
        encoded = ''.join(encode(stream))
        enc_len = len(encoded)
        flippy = [()]
        for i in range(enc_len):
            flippy.append((i, ))
            for j in range(i + 1, enc_len):
                flippy.append((i, j))
                for k in range(j + 1, enc_len):
                    flippy.append((i, j, k))
                    for l in range(k + 1, enc_len):
                        flippy.append((i, j, k, l))
                        for m in range(l + 1, enc_len):
                            flippy.append((i, j, k, l, m))
                            for n in range(m + 1, enc_len):
                                flippy.append((i, j, k, l, m, n))
                                for o in range(n + 1, enc_len):
                                    flippy.append((i, j, k, l, m, n, o))
                                    for p in range(o + 1, enc_len):
                                        flippy.append((i, j, k, l, m, n, o, p))

        for flip in flippy:
            copy = [int(c) for c in encoded]
            prob = pow(0.001, len(flip)) * pow(0.999, 8 - len(flip))
            for f in flip:
                copy[f] = 1 - copy[f]  # flip it
            noised = ''.join(str(c) for c in copy)
            decoded = ''.join(decode(MockStdIn(noised)))
            failure = 0.
            for enc, dec in zip(number, decoded):
                if enc != dec:
                    failure += 1
            total_failure += prob * (failure / 4)
        print(total_failure)
        self.assertTrue(False)

    @unittest.skip
    def test_04(self):
        """Test with 0.4 probability."""
        successes, failures = self.bit_error(0.4)
        msg = '\nsuccesses: {}\nfailures: {}'.format(successes, failures)
        self.assertTrue(False, msg=msg)

    @unittest.skip
    def test_01(self):
        """Test with 0.1 probability."""
        successes, failures = self.bit_error(0.1)
        msg = '\nsuccesses: {}\nfailures: {}'.format(successes, failures)
        self.assertTrue(False, msg=msg)

    @unittest.skip
    def test_0001(self):
        """Test with 0.001 probability."""
        successes, failures = self.bit_error(0.001)
        msg = '\nsuccesses: {}\nfailures: {}'.format(successes, failures)
        self.assertTrue(False, msg=msg)


if __name__ == '__main__':
    unittest.main()
