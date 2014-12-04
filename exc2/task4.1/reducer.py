#!/usr/bin/env python2.7

import sys
import heapq


HEAP = []
N = 10

for line in sys.stdin:
    question, count = line.strip().split('\t')
    count = int(count)
    if len(HEAP) == N:
        # if heap full, pop smallest
        heapq.heappushpop(HEAP, (count, question))
    else:
        # if not full, just push
        heapq.heappush(HEAP, (count, question))

# HEAP now has top 10 questions
for count, question in HEAP:
    print('{0},\t{1}'.format(question, count))

