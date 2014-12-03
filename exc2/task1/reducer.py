#!/usr/bin/env python3

import sys

from collections import Counter


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
    print('{0}:\t{1}\t{2}'.format(word, len(counts), sorted(counts.items())))

