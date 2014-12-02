#!/usr/bin/python

import sys
import heapq

DEFAULT_N = 20

prev_triple = None
total_count = 0

heap = []


def heap_add(heap, item):
    """Adds item onto heap if not full."""
    if len(heap) < DEFAULT_N:
        # if not full just push
        heapq.heappush(heap, item)
    else:
        # if full also pop
        heapq.heappushpop(heap, item)


for line in sys.stdin:
    triple, count = line.strip().split('\t')
    count = int(count)
    if triple == prev_triple:
        # aggregate count
        total_count += count
    else:
        # different triple -> print previous
        if prev_triple is not None:
            heap_add(heap, (total_count, prev_triple))
        # and update previous
        prev_triple = triple
        total_count = count

# add last one if not added yet
if prev_triple == triple:
    heap_add(heap, (total_count, prev_triple))

# print top 20 triples
for total_count, triple in heapq.nlargest(DEFAULT_N, heap):
    print('{0}\t{1}'.format(triple, total_count))
