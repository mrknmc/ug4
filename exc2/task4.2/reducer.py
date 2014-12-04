#!/usr/bin/env python3

import sys

from itertools import chain, groupby
from operator import itemgetter


def parse(stream):
    for line in stream:
        owner, *qs = line.strip().split('\t')
        yield owner, qs


max_owner = None
max_qs = []

for owner, q_lists in groupby(parse(sys.stdin), key=itemgetter(0)):
    questions = list(chain(*(q_list for owner, q_list in q_lists)))
    if len(questions) > len(max_qs):
        max_owner = owner
        max_qs = questions

if max_owner is not None:
    print('{0}\t->\t{1}'.format(max_owner, ', '.join(max_qs)))

