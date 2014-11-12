import unittest
import math

from count import *


class Test(unittest.TestCase):

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


if __name__ == '__main__':
    unittest.main()
