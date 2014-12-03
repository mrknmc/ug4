#!/usr/bin/env python3

import sys

from itertools import groupby
from operator import itemgetter


def parse(stream):
    for line in stream:
        host, tstamp = line.split(' ', 1)
        yield host, int(tstamp)


for host, tstamps in groupby(parse(sys.stdin), key=itemgetter(0)):
    min_tstamp = next(tstamps)[1]
    max_tstamp = None
    for host, tstamp in tstamps:
        max_tstamp = tstamp
    if max_tstamp is not None:
        # no max found => only one timestamp
        print('{0}\t{1}'.format(host, max_tstamp - min_tstamp))
    else:
        print('{0}\t{1}'.format(host, min_tstamp))

