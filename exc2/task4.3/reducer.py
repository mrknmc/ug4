#!/usr/bin/env python3

import sys

from itertools import chain, groupby
from operator import itemgetter


def parse(stream):
    for line in stream:
        keys, *vals = line.strip().split('\t')
        question, typ = keys.split(' ')
        yield question, typ, vals 


def accepted(stream):
    for question, vals in groupby(parse(stream), key=itemgetter(0)):
        # first should be the question
        question, typ, rest = next(vals)
        if typ != '1':
            # not a question => answers but no question
            continue
        accepted_answer = rest[0]
        for q, typ, rest in vals:
            # find user who submitted accepted answer
            if typ == '2':
                answer, user = rest
                if answer == accepted_answer:
                    yield user, accepted_answer
                    break


for user, answers in groupby(accepted(sys.stdin), key=itemgetter(0)):
    print('{0}\t{1}'.format(user, '\t'.join(answer for user, answer in answers)))
