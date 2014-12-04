#!/usr/bin/env python3

import sys

from itertools import chain, groupby
from operator import itemgetter


def parse(stream):
    for line in stream:
        # one line could contain multiple answers
        owner, *answers = line.strip().split('\t')
        yield owner, answers


max_owner = None
max_answers = []

for owner, a_lists in groupby(parse(sys.stdin), key=itemgetter(0)):
    answers = list(chain(*(a_list for owner, a_list in a_lists)))
    if len(answers) > len(max_answers):
        max_owner = owner
        max_answers = answers

if max_owner is not None:
    print('{0}\t->\t{1},\t{2}'.format(max_owner, len(max_answers), ', '.join(max_answers)))

