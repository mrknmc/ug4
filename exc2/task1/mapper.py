#!/usr/bin/env python2.7

import sys
import os

from collections import Counter

INPUT_FILE = os.getenv('map_input_file').rsplit('/', 1)[1]

# TODO: could store the whole file in a dictionary
# and spit out counts if it gets full

for line in sys.stdin:
    tokens = line.strip().split()
    counter = Counter(tokens)
    for token, count in counter.items():
        print('{0} {1}\t{2}'.format(token, INPUT_FILE, count))

