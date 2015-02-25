import unittest

from cache import coherence


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
        gen = coherence(instrs, DEFAULT_LINES, DEFAULT_WORDS, mesi)
        for caches, state in zip(gen, states):
            cache_id, addr, state = state
            index = addr % DEFAULT_LINES
            cache = caches[cache_id]
            self.assertEqual(cache[index]['state'], state)

    def test_msi_instructions(self):
        self.instructions(INSTRS, MSI_STATES, False)

    def test_mesi_instructions(self):
        self.instructions(INSTRS, MESI_STATES, True)


if __name__ == '__main__':
    unittest.main()
