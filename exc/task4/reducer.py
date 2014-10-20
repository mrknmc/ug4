#!/usr/bin/python

import sys

prev_triple = None
total_count = 0

for line in sys.stdin:
    triple, count = line.strip().split('\t')
    count = int(count)
    if triple == prev_triple:
        total_count += count
    else:
        if prev_triple is not None:
            print('{0}\t{1}'.format(prev_triple, total_count))
        prev_triple = triple
        total_count = count

if prev_triple == triple:
    print('{0}\t{1}'.format(triple, total_count))
