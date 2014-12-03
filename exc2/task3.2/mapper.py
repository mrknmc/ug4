#!/usr/bin/env python3

import sys
import re

from itertools import groupby
from operator import itemgetter


def parse(stream):
    for line in stream:
        match = re.match(r'^\s*(.*?)\s+- -\s+?\[(.*?)\]\s*?"([A-Z]+)\s+?(.*?)\s+?(.+?)"\s+(\d+)\s+(\d+|-)\s*$', line)
        if match is not None:
            groups = match.groups()
            status = groups[5]
            if status == '404':
                yield groups


for host, reqs in groupby(parse(sys.stdin), key=itemgetter(0)):
    print('{0}\t{1}'.format(host, sum(1 for req in reqs))) 
