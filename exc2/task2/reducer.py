#!/usr/bin/env python3

import sys
import math

from collections import Counter

N = 17

TERMS = set()

with open('terms.txt') as terms_file:
    for term in terms_file:
        TERMS.add(term.strip())


def parse(stream):
    counts = Counter()
    prev_word = None
    for line in stream:
        keys, count = line.split('\t', 1)
        word, doc = keys.split(' ', 1)
        if word == prev_word:
            counts[doc] += int(count)
        else:
            # word change, yield previous word
            if prev_word is not None:
                yield prev_word, counts
                counts.clear()
            prev_word = word
            counts[doc] += int(count)
    if counts:
        yield word, counts


for word, counts in parse(sys.stdin):
    occurences = len(counts)
    TERMS.discard(word)
    doc = 'd1.txt'
    count = counts[doc]
    tf = count
    idf = math.log10(N / (1. + occurences))
    print('{0}, {1} = {2}'.format(word, doc, tf * idf))

for word in TERMS:
    print('{0}, {1} = {2}'.format(word, 'd1.txt', 0))

