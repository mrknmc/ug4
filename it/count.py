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


def unigen(file_):
    """Takes a file and turns it into a character generator, ignoring \n."""
    prog = re.compile(r'[a-z ]')
    return (c.lower() for c in chain(*file_) if prog.match(c))


def bigen(file_):
    """Bigram generator from a file."""
    file1, file2 = [unigen(file_gen) for file_gen in tee(file_)]
    next(file2)  # drop first char
    return zip(file1, file2)


def unigram(file_):
    """Computes the bigram distribution of a file."""
    counter = Counter(unigen(file_))
    chars = sum(counter.values())
    return {key: (val / float(chars)) for key, val in counter.items()}


def bigram(file_):
    """Computes the bigram distribution of a file."""
    counter = Counter(bigen(file_))
    chars = sum(counter.values())
    return {key: (val / float(chars)) for key, val in counter.items()}


def iid_length(file_, dist):
    """Length of a file if its chars were i.i.d."""
    probs = (dist[c] for c in unigen(file_))
    file_len = -sum(math.log(prob, 2) for prob in probs)
    return int(math.ceil(file_len + 2))


def bi_length(file_, uni_dist, bi_dist):
    """Length of a file if its chars were bigramy."""
    chars = list(bigen(file_))
    char1 = chars[0][0]
    probs = [bi_dist[cs] / uni_dist[cs[0]] for cs in chars]
    probs.append(uni_dist[char1])
    file_len = - sum(math.log(prob, 2) for prob in probs)
    return int(math.ceil(file_len + 2))


def iid_round_length(file_, dist, bits=8):
    """"""
    pow2 = pow(2, bits)
    # rounding
    round_dist = {k: math.ceil(pow2 * p) / pow2 for k, p in dist.items()}
    # normalizing sum
    round_sum = sum(p for p in round_dist.values())
    # renormalizing
    round_dist = {k: p / round_sum for k, p in round_dist.items()}
    # each char needs bits in header
    header = len(round_dist.keys()) * bits
    data = iid_length(file_, dist)
    return {'header': header, 'data': data, 'total': header + data}


def bi_round_length(file_, uni_dist, bi_dist, bits=8):
    """"""
    pow2 = pow(2, bits)
    # rounding
    round_dist = {k: math.ceil(pow2 * p) / pow2 for k, p in dist.items()}
    # normalizing sum
    round_sum = sum(p for p in round_dist.values())
    # renormalizing
    round_dist = {k: p / round_sum for k, p in round_dist.items()}
    # each char needs bits in header
    header = len(round_dist.keys()) * bits
    data = iid_length(file_, dist)
    return {'header': header, 'data': data, 'total': header + data}


def main():
    """Do the thing."""
    with open(FILE) as file_:
        uni_dist = unigram(file_)
        ent_x = entropy(uni_dist)
        print('H(X_n): {0:.4}'.format(ent_x))

        file_.seek(0)
        bi_dist = bigram(file_)
        ent_joint = entropy(bi_dist)
        print('H(X_n, X_n+1): {0:.4}'.format(ent_joint))
        ent_cond = ent_joint - ent_x
        print('H(X_n+1 | X_n): {:.4}'.format(ent_cond))

        file_.seek(0)
        iid_len = iid_length(file_, uni_dist)
        print('i.i.d. length: {}'.format(iid_len))

        file_.seek(0)
        bi_len = bi_length(file_, uni_dist, bi_dist)
        print('bigram length: {}'.format(bi_len))

        file_.seek(0)
        iid_round_len = iid_round_length(file_, uni_dist)
        print('i.i.d. length rounded:\n\theader: {header}\n\tdata: {data}\n\ttotal: {total}'.format(**iid_round_len))

        file_.seek(0)
        bi_round_len = bi_round_length(file_, uni_dist)
        print('i.i.d. length rounded:\n\theader: {header}\n\tdata: {data}\n\ttotal: {total}'.format(**bi_round_len))

if __name__ == '__main__':
    main()
