#!/usr/bin/env python3

import sys

from itertools import chain, groupby
from operator import itemgetter


def parse(stream):
    for line in stream:
        yield line.strip().split('\t')


def accepted(stream):
    for question, vals in groupby(parse(stream), key=itemgetter(0)):
        # first should be the question
        question, typ, *rest = next(vals)
        if typ != '1':
            # it was not a question
            # there are answers but no question
            continue
        accepted_answer = rest[0]
        accepted_user = None
        # find user who submitted accepted answer
        for q, typ, answer, user, in vals:
            if typ == '2' and answer == accepted_answer:
                accepted_user = user
                # found him
                yield accepted_user, accepted_answer
                break


for user, answers in groupby(accepted(sys.stdin), key=itemgetter(0)):
    print('{0}\t{1}'.format(user, '\t'.join(answer for user, answer in answers)))
