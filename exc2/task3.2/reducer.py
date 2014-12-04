#!/usr/bin/env python3

import sys
import heapq

from itertools import groupby
from operator import itemgetter


HEAP = []
N = 10


def parse(stream):
    for line in stream:
        host, count = line.split('\t', 1)
        yield host, int(count)


for url, counts in groupby(parse(sys.stdin), key=itemgetter(0)):
    total_count = sum(count for url, count in counts)
    if len(HEAP) == N:
        # if heap full, pop smallest
        heapq.heappushpop(HEAP, (total_count, url))
    else:
        # if not full, just push
        heapq.heappush(HEAP, (total_count, url))

# HEAP now has top 10 questions
for count, url in HEAP:
    print('{0}\t{1}'.format(url, count))

