#!/usr/bin/env python3

import sys
import math

from itertools import groupby
from operator import itemgetter

N = 17
DOC = 'd1.txt'
TERMS = set()


def parse(stream):
    for line in stream:
        keys, count = line.split('\t', 1)
        word, doc = keys.split(' ', 1)
        yield word, doc, int(count)


with open('terms.txt') as terms_file:
    for term in terms_file:
        TERMS.add(term.strip())

for word, counts in groupby(parse(sys.stdin), key=itemgetter(0)):
    TERMS.discard(word)
    counter = {}
    # next group by doc
    for (word, doc), meh in groupby(counts, key=itemgetter(0, 1)):
        counter[doc] = sum(count for (word, doc, count) in meh)
    occurences = len(counter)
    tf = counter.get(DOC, 0)
    idf = math.log10(N / (1. + occurences))
    print('{0}, {1} = {2}'.format(word, DOC, tf * idf))

for word in TERMS:
    print('{0}, {1} = {2}'.format(word, DOC, 0))

