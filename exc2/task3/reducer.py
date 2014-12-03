#!/usr/bin/env python3

import sys

from itertools import groupby
from operator import itemgetter


def parse(stream):
    for line in stream:
        yield line.split('\t', 1)


for url, counts in groupby(parse(sys.stdin), key=itemgetter(0)):
    print('{0}\t{1}'.format(url, sum(int(count) for url, count in counts)))

