#!/usr/bin/env python3

import sys

from itertools import groupby
from operator import itemgetter


def parse(stream):
    for line in stream:
        url, count = line.split('\t', 1)
        yield url, int(count)


max_url = None
max_count = 0

for url, counts in groupby(parse(sys.stdin), key=itemgetter(0)):
    total_count = sum(count for url, count in counts)
    if total_count > max_count:
        max_url = url
        max_count = total_count

if max_url is not None:
    print('{0}\t{1}'.format(max_url, max_count))

