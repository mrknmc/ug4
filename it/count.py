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


def information_content(dist):
    """Computes the information content of a distribution."""
    return sum(-math.log(prob, 2) for prob in dist.values())


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
    file_len = -sum(math.log(prob, 2) for prob in probs)
    return int(math.ceil(file_len + 2))


def round_dist(dist, bits=8):
    """Round and renormalize a distribution."""
    pow2 = pow(2, bits)
    # rounding
    round_dist = {k: math.ceil(pow2 * p) / pow2 for k, p in dist.items()}
    # normalizing sum
    round_sum = sum(p for p in round_dist.values())
    # renormalizing
    return {k: p / round_sum for k, p in round_dist.items()}


def iid_round_length(file_, dist, bits=8):
    """How long the file would be if we used a rounding scheme."""
    rounded_dist = round_dist(dist)
    # each char needs bits in header
    # TODO: consider changing below to 27 * bits
    header = len(rounded_dist.keys()) * bits
    data = iid_length(file_, rounded_dist)
    return {'header': header, 'data': data, 'total': header + data}


def bi_round_length(file_, uni_dist, bi_dist, bits=8):
    """How long the file would be if we used a rounding scheme."""
    # TODO: If conditional then, 1,151,752
    uni_rounded_dist = round_dist(uni_dist)
    bi_rounded_dist = round_dist(bi_dist)
    # each pair of chars needs bits in header + first char
    # TODO: change below to 27 * 27
    header = bits + len(bi_rounded_dist.keys()) * bits
    data = bi_length(file_, uni_rounded_dist, bi_rounded_dist)
    return {'header': header, 'data': data, 'total': header + data}


def iid_adapt_length(f):
    """Compression with adaptation using Laplace prediction rule."""
    count = Counter()
    file_len = 0.0
    for n, char in enumerate(unigen(f), start=0):
        k_i = count.get(char, 0)
        prob = (k_i + 1.0) / (n + 27)
        file_len -= math.log(prob, 2)
        count[char] += 1

    return int(math.ceil(file_len + 2))


def bigram_adapt_length(f):
    """Compression with adaptation using prediction rule for bigram model."""
    k = Counter()
    n = Counter()
    file_len = 0.0
    prev = None
    for char in unigen(f):
        k_ij = k.get((prev, char), 0)
        n_j = n.get(prev, 0)
        prob = (k_ij + 1.0) / (n_j + 27)
        file_len -= math.log(prob, 2)
        k[(prev, char)] += 1
        n[prev] += 1
        prev = char

    return int(math.ceil(file_len + 2))


def nutritious_snacks(chars, nums):
    """XOR's nutritious snacks with some numbers."""
    return ''.join(chr(ord(char) ^ num) for char, num in zip(chars, nums))


def main():
    """Do the thing."""
    with open(FILE) as f:
        uni_dist = unigram(f)
        ent_x = entropy(uni_dist)
        print('H(X_n): {0:.4}'.format(ent_x))

        f.seek(0)
        bi_dist = bigram(f)
        ent_joint = entropy(bi_dist)
        print('H(X_n, X_n+1): {0:.4}'.format(ent_joint))
        ent_cond = ent_joint - ent_x
        print('H(X_n+1 | X_n): {:.4}'.format(ent_cond))

        f.seek(0)
        iid_len = iid_length(f, uni_dist)
        print('i.i.d. length: {}'.format(iid_len))

        f.seek(0)
        bi_len = bi_length(f, uni_dist, bi_dist)
        print('bigram length: {}'.format(bi_len))

        f.seek(0)
        iid_round_len = iid_round_length(f, uni_dist)
        print('i.i.d. length rounded:\n\theader: {header}\n\tdata: {data}\n\ttotal: {total}'.format(**iid_round_len))

        f.seek(0)
        bi_round_len = bi_round_length(f, uni_dist, bi_dist)
        print('bigram length rounded:\n\theader: {header}\n\tdata: {data}\n\ttotal: {total}'.format(**bi_round_len))

        f.seek(0)
        iid_adapt_len = iid_adapt_length(f)
        print('i.i.d. adaptation: {}'.format(iid_adapt_len))

        f.seek(0)
        bi_adapt_len = bigram_adapt_length(f)
        print('bigram adaptation: {}'.format(bi_adapt_len))

        snacks_xor = nutritious_snacks(
            'nutritious snacks',
            [59, 6, 17, 0, 83, 84, 26, 90, 64, 70, 25, 66, 86, 82, 90, 95, 75]
        )
        print('nutritious_snacks XOR: {}'.format(snacks_xor))


if __name__ == '__main__':
    main()
