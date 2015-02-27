import pprint
import unittest

from collections import defaultdict
from itertools import islice
from cache import coherence, get_state, make_line, Line


DEFAULT_LINES = 1024
DEFAULT_WORDS = 4


INSTRS = [
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

MSI_STATES = [
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

MESI_STATES = [
    (0, 20, 'E'),  # miss
    (0, 20, 'E'),  # hit (in Shared/Exclusive)
    (0, 10, 'E'),  # miss
    (0, 10, 'E'),  # hit (in Shared/Exclusive)
    (1, 10, 'M'),  # miss
    (1, 10, 'M'),  # hit (in Modified)
    (1, 30, 'M'),  # miss
    (1, 30, 'M'),  # hit (in Modified)
    (0, 30, 'S'),  # miss
    (1, 30, 'S'),  # hit (in Shared)
    (0, 30, 'S'),  # hit (in Shared)
]


class Test(unittest.TestCase):
    """"""

    def instructions(self, instrs, states, mesi):
        """Test that after executing an instruction
        from instrs it corresponds to state in states."""
        gen = coherence(instrs, DEFAULT_LINES, DEFAULT_WORDS, mesi, None)
        for (caches, metrics), state in zip(gen, states):
            cache_id, addr, state = state
            line = make_line(addr, DEFAULT_WORDS, DEFAULT_LINES)
            cache = caches[cache_id]
            self.assertEqual(cache[line.index]['state'], state)

    def test_eviction(self):
        """After eviction state is None and not previous line's state."""
        instrs = ('P0 R 0', 'P0 R 1024')
        gen = coherence(instrs, DEFAULT_LINES, DEFAULT_WORDS, False, None)
        caches, metrics = next(gen)
        state = get_state(caches[0], Line(0, 1))
        self.assertEqual(state, None)

    def test_address_translation(self):
        """Test that addresses are translated to an index and tag correctly."""
        addresses = {
            0: (0, 0),
            3: (0, 0),

        }
        for addr, (index, tag) in addresses.items():
            line = make_line(addr, DEFAULT_WORDS, DEFAULT_LINES)
            self.assertEqual(line.index, index)
            self.assertEqual(line.tag, tag)

    def test_msi_instructions(self):
        self.instructions(INSTRS, MSI_STATES, False)

    def test_mesi_instructions(self):
        self.instructions(INSTRS, MESI_STATES, True)


if __name__ == '__main__':
    unittest.main()
