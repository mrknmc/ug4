"""
"""

import re
import math

from itertools import tee, chain
from collections import Counter


FILE = 'thesis.txt'


def entropy(dist):
    """Computes the entropy of a distribution."""
    return sum(-prob * math.log(prob, 2) for prob in dist.values())


def unigram(file_):
    """Computes the bigram distribution of a file."""
    counter = Counter(char_gen(file_))
    chars = sum(counter.values())
    return {key: (val / float(chars)) for key, val in counter.items()}


def char_gen(file_):
    """Takes a file and turns it into a character generator, ignoring \n."""
    prog = re.compile(r'[a-z ]')
    return (c.lower() for c in chain(*file_) if prog.match(c))


def bigram(file_):
    """Computes the bigram distribution of a file."""
    file1, file2 = [char_gen(file_gen) for file_gen in tee(file_)]
    next(file2)  # drop first char
    counter = Counter(zip(file1, file2))
    chars = sum(counter.values())
    return {key: (val / float(chars)) for key, val in counter.items()}


def main():
    """Do the thing."""
    with open(FILE) as file_:
        file1, file2 = tee(file_)
        uni_dist = unigram(file1)
        ent_x = entropy(uni_dist)
        print('{0:.4}'.format(ent_x))
        bi_dist = bigram(file2)
        ent_joint = entropy(bi_dist)
        print('{0:.4}'.format(ent_joint))
        ent_cond = ent_joint - ent_x
        print('{:.4}'.format(ent_cond))


if __name__ == '__main__':
    main()
