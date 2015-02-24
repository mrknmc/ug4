import math
import unittest

from cache import coherence, make_instruction


DEFAULT_LINES = 1024
DEFAULT_WORDS = 4


class Test(unittest.TestCase):
    """"""

    instrs = [
        'P0 R 20',
        'P0 R 20',
        'P0 R 10',
        'P0 R 10',
        'P1 W 10',
        'P1 R 10',
        'P1 W 30',
        'P1 W 30',
        'P0 R 30',
        'P1 R 30',
        'P0 R 30',
    ]

    states = [
        (0, 20, 'S'),  # miss
        (0, 20, 'S'),  # hit (in Shared/Exclusive)
        (0, 10, 'S'),  # miss
        (0, 10, 'S'),  # hit (in Shared/Exclusive)
        (1, 10, 'M'),  # miss
        (1, 10, 'M'),  # hit (in Modified)
        (1, 30, 'M'),  # miss
        (1, 30, 'M'),  # hit (in Modified)
        (0, 30, 'S'),  # miss
        (1, 30, 'S'),  # hit (in Shared)
        (0, 30, 'S'),  # hit (in Shared)
    ]

    def test_make_instruction(self):
        lines = 1024
        index_size = int(math.log(lines, 2))
        line = 'P1 W 5379'
        inst = make_instruction(line, index_size)

        rem = 5379 % 1024
        self.assertEqual(rem, inst.index)
        print(5379 / 1024.0)
        print(inst.tag, inst.index)
        self.assertFalse(True)

    def test_instrs(self):
        for caches, state in zip(coherence(self.instrs, DEFAULT_LINES, DEFAULT_WORDS), self.states):
            cache_id, addr, state = state
            index = addr % DEFAULT_LINES
            cache = caches[cache_id]
            # check the state
            self.assertEqual(cache[index]['state'], state)


if __name__ == '__main__':
    unittest.main()
