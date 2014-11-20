"""
"""

import re
import math

from itertools import tee, chain
from collections import Counter, defaultdict


FILE = 'thesis.txt'
ALPHABET_SIZE = 27


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


def cond_dist(uni_dist, bi_dist):
    """Creates conditional distribution from i.i.d. and joint dists."""
    return {(c0, c1): bi_dist[c0, c1] / uni_dist[c0] for (c0, c1) in bi_dist}


def norm_dist(dist):
    """Normalise a distribution."""
    round_sum = sum(dist.values())
    return {k: p / round_sum for k, p in dist.items()}


def round_dist(dist, bits=8):
    """Round a distribution."""
    pow2 = pow(2, bits)
    return {k: math.ceil(pow2 * p) / pow2 for k, p in dist.items()}


def norm_cond_dist(dist):
    """Normalise a conditional distribution."""
    # turn into temporary form
    d = defaultdict(Counter)
    for (c0, c1), prob in dist.items():
        d[c0][c1] = prob

    for c0 in d:
        total = 0.
        # sum up conditional probs
        for c1, prob in d[c0].items():
            total += prob
        # normalise
        for c1 in d[c0]:
            d[c0][c1] /= total

    # turn back to original form
    v = Counter()
    for c0 in d:
        for c1 in d[c0]:
            v[c0, c1] = d[c0][c1]
    return v


def iid_round_length(file_, dist, bits=8):
    """How long the file would be if we used a rounding scheme."""
    rounded_dist = norm_dist(round_dist(dist))
    # each char needs bits in header
    header = ALPHABET_SIZE * bits
    data = iid_length(file_, rounded_dist)
    return {'header': header, 'data': data, 'total': header + data}


def bi_round_length(file_, uni_dist, bi_dist, bits=8):
    """How long the file would be if we used a rounding scheme."""
    # TODO: If conditional then, 1,151,752
    uni_rounded_dist = norm_dist(round_dist(uni_dist))
    conditional_dist = cond_dist(uni_dist, bi_dist)
    cond_rounded_dist = round_dist(conditional_dist)
    cond_rounded_dist = norm_cond_dist(cond_rounded_dist)
    chars = list(bigen(file_))
    char1 = chars[0][0]
    probs = [cond_rounded_dist[cs] for cs in chars]
    probs.append(uni_rounded_dist[char1])
    file_len = -sum(math.log(prob, 2) for prob in probs)
    data = int(math.ceil(file_len + 2))
    # each pair of chars needs bits in header
    header = (1 + ALPHABET_SIZE) * ALPHABET_SIZE * bits
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
    """XORs nutritious snacks with some numbers."""
    return ''.join(chr(ord(char) ^ num) for char, num in zip(chars, nums))


def digital_fountain(pkts, recvd):
    """Performs the digital fountain algorithm on packets."""
    rec_len = len(recvd)
    result = [None] * rec_len
    used_pkts = []
    while 1:
        empty_count = 0
        for idx, (rec, packet) in enumerate(zip(recvd, pkts), start=1):
            if len(packet) == 0:
                empty_count += 1
            elif len(packet) == 1:
                # we know what the char is
                num = packet.pop()
                result[num - 1] = chr(rec)  # -1 b/c zero indexing
                used_pkts.append(idx)
                for j, pkt in enumerate(pkts):
                    if num in pkt:
                        if len(pkt) == 1:
                            # packet redundant
                            pkt.discard(num)
                        elif len(pkt) > 1:
                            # XOR the char we know
                            pkt.discard(num)
                            recvd[j] ^= rec

        if empty_count == rec_len:
            break  # if all empty -> finish
    result = ''.join(res for res in result if res is not None)
    return result, used_pkts


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
        print("""i.i.d. length rounded:
\theader: {header}
\tdata: {data}
\ttotal: {total}""".format(**iid_round_len))

        f.seek(0)
        bi_round_len = bi_round_length(f, uni_dist, bi_dist)
        print("""bigram length rounded:
\theader: {header}
\tdata: {data}
\ttotal: {total}""".format(**bi_round_len))

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

    with open('packets.txt') as pkts, open('received.txt') as recvd:
        pkts = [set(map(int, line.split())) for line in pkts]
        recvd = [int(line) for line in recvd]
        source_str, used_pkts = digital_fountain(pkts, recvd)
        print('Source string: {}'.format(source_str))
        print('Packets used: {}'.format(' '.join(map(str, used_pkts))))


if __name__ == '__main__':
    main()
