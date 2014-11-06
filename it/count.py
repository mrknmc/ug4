"""
"""

from math import log
from itertools import tee, chain
from collections import Counter


FILE = 'thesis.txt'


def entropy(dist):
    """Computes the entropy of a distribution."""
    return sum(-prob * log(prob, 2) for prob in dist.values())


def unigram(file_):
    """Computes the bigram distribution of a file."""
    counter = Counter(char_gen(file_))
    chars = sum(counter.values())
    return {key: (val / float(chars)) for key, val in counter.items()}


def char_gen(file_):
    """Takes a file and turns it into a character generator, ignoring \n."""
    return filter(lambda c: c != '\n', chain(*file_))


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
        methods = [unigram, bigram]
        for method, f in zip(methods, tee(file_, len(methods))):
            dist = method(f)
            print(dist)
            ent = entropy(dist)
            print('{0:.4}'.format(ent))


if __name__ == '__main__':
    main()
