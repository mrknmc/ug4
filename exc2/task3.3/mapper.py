#!/usr/bin/env python3

import sys
import re

from datetime import datetime
from itertools import groupby
from operator import itemgetter


def parse(stream):
    for line in stream:
        match = re.match(r'^\s*(.*?)\s+- -\s+?\[(.*?)\]\s*?"([A-Z]+)\s+?(.*?)\s+?(.+?)"\s+(\d+)\s+(\d+|-)\s*$', line)
        if match is not None:
            yield match.groups()


for host, reqs in groupby(parse(sys.stdin), key=itemgetter(0)):
    # set min and max to None
    min_tstamp = max_tstamp = None 
    for req in reqs:
        date = datetime.strptime(req[1], '%d/%b/%Y:%H:%M:%S %z')
        # safe casting to int bc no milliseconds
        tstamp = int(date.timestamp())
        if max_tstamp is None or tstamp > max_tstamp:
            max_tstamp = tstamp
        elif min_tstamp is None or tstamp < min_tstamp: 
            min_tstamp = tstamp
    if min_tstamp is not None:
        print('{0} {1}'.format(host, min_tstamp))
    if max_tstamp is not None:
        print('{0} {1}'.format(host, max_tstamp))

