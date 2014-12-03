#!/usr/bin/env python3

import sys

from itertools import groupby
from operator import itemgetter


def parse(stream):
    for line in stream:
        keys, count = line.split('\t', 1)
        word, doc = keys.split(' ', 1)
        yield word, doc, int(count)


# first group by word
for word, counts in groupby(parse(sys.stdin), key=itemgetter(0)):
    counter = []
    # next group by doc
    for (word, doc), meh in groupby(counts, key=itemgetter(0, 1)):
        word_freq = sum(count for (word, doc, count) in meh)
        counter.append((doc, word_freq))

    print('{0}:\t{1}:\t{2}'.format(word, len(counter), counter))

