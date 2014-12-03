#!/usr/bin/env python2.7

import sys
import re

from itertools import groupby
from operator import itemgetter


def parse(stream):
    for line in stream:
        match = re.match(r'^\s*(.*?)\s+- -\s+?\[(.*?)\]\s*?"([A-Z]+)\s+?(.*?)\s+?(.+?)"\s+(\d+)\s+(\d+|-)\s*$', line)
        if match is not None:
            yield match.groups()


for url, reqs in groupby(parse(sys.stdin), key=itemgetter(3)):
    print('{0}\t{1}'.format(url, len(list(reqs)))) 