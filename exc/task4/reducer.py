#!/usr/bin/python

import sys

prev_triple = None
count = 0

for line in sys.stdin:
    triple, count = line.strip().split('\t')
    count = int(count)
    if triple == prev_triple:
        count += 1
    else:
        if prev_triple is not None:
            print('{0}\t{1}'.format(prev_triple, count))
        prev_triple = triple
        count = 0

if prev_triple == triple:
    print('{0}\t{1}'.format(triple, count))
