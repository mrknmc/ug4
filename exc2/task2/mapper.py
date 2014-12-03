#!/usr/bin/env python3

import sys
import os

from collections import Counter

INPUT_FILE = os.getenv('map_input_file').rsplit('/', 1)[1]
TERMS = set()

with open('terms.txt') as terms_file:
    for term in terms_file:
        TERMS.add(term.strip())

for line in sys.stdin:
    tokens = line.strip().split()
    counter = Counter(token for token in tokens if token in TERMS)
    for token, count in counter.items():
        print('{0} {1}\t{2}'.format(token, INPUT_FILE, count))

