import math
import hashlib
import re
import sys

from itertools import izip
from contextlib import nested
from collections import defaultdict


COUPLE_THRESH = 3
DEFAULT_K = 16
DEFAULT_C = 100
HASH_SIZE = 128
STOP_WORDS = [word.rstrip('\n') for word in open('english.txt')]


class Doc(dict):
    """Dict wrapper that represents a document in the collection."""

    def __init__(self, id_, tokens):
        self.id = id_
        m = hashlib.md5()
        for token in tokens:
            m.update(token)
            # skip stop words but add them to the hash
            if token not in STOP_WORDS and token != '':
                self.setdefault(token, 0)
                self[token] += 1.0
        self.hash = m.digest()
        self.dist = math.sqrt(sum(freq * float(freq) for freq in self.itervalues()))


def parse(file_):
    """Parses the file, tokenizes and removes stop words."""
    for line in file_:
        story_id, rest = line.strip().lower().split(' ', 1)
        tokens = re.split(r'[\t\r\n\\~`!@#$%^&*\(\)_\-+=\[\]\{\}|:;"\'<>,.?/ ]+', rest)
        yield Doc(story_id, tokens)


def is_number(token):
    """Checks whether a token is a number."""
    return re.match(r'\d+', token) is not None


def comparator(story_id):
    """Return the int value from a story id."""
    return int(story_id.lstrip('t'))


def similarity(doc1, doc2):
    """Cosine similarity measure."""
    qw_dw = 0.0
    for word, tf_wq in doc1.iteritems():
        if word in doc2:
            qw_dw += tf_wq * doc2[word]
    return qw_dw / (doc1.dist * doc2.dist)


def hash_word(word):
    """Hashes a word into a binary sequence."""
    digest = hashlib.md5(word).digest()
    return ''.join(bin(ord(char)).lstrip('0b').zfill(8) for char in digest)


def simhash(doc, k):
    """Hashes a document using simhash."""
    # make array to store results
    hash_sum = [0] * HASH_SIZE
    for word, freq in doc.iteritems():
        # compute hash for every word
        word_hash = hash_word(word)
        assert len(word_hash) == HASH_SIZE
        for idx, char in enumerate(word_hash):
            # sum char vals in each column
            hash_sum[idx] += freq if char == '1' else -freq
    # combine into a binary string
    fingerprint = ''.join('1' if hsum > 0 else '0' for hsum in hash_sum)
    return (fingerprint[k * i:k * (i + 1)] for i in range(len(fingerprint) / k))


def finn_parse(file_):
    """Extracts areas with many numbers from a document."""
    for line in file_:
        story_id, rest = line.strip().lower().split(' ', 1)
        tokens = re.split(r'[\t\r\n\\~`!@#$%^&*\(\)_\-+=\[\]\{\}|:;"\'<>,.?/ ]+', rest)
        S = s = best = a = b = 0
        for idx, token in enumerate(tokens):
            val = 0 if is_number(token) else 1
            S += DEFAULT_C * (1 - val) - val
            if S <= 0:
                s = idx + 1
                S = 0
            if S > best:
                a = s
                b = idx
                best = S
        if b - a < COUPLE_THRESH:
            continue
        yield Doc(story_id, tokens[a:b])


def get_similar(doc, buckets, k):
    """Return document ids that are in the same bucket and their similarity."""
    # compute the fingerprint hashes
    similar = set()
    hashes = simhash(doc, k)
    for bucket, hash_ in izip(buckets, hashes):
        if hash_ in bucket:
            for seen_doc in bucket[hash_]:
                if seen_doc.id not in similar:
                    if doc.hash == seen_doc.hash:
                        # -1.0 special value for identical
                        similar.add((seen_doc.id, -1.0))
                    else:
                        sim = similarity(doc, seen_doc)
                        if sim > 0.8:
                            similar.add((seen_doc.id, sim))
        bucket[hash_].append(doc)
    return similar


def main(k):
    with nested(
        open('data.train'),
        open('type1.dup', 'w'),
        open('type2.dup', 'w'),
    ) as (train, type1, type2):
        buckets = [defaultdict(list) for i in range(HASH_SIZE / k)]
        for doc in parse(train):
            similar = get_similar(doc, buckets, k)
            for seen_story_id, sim in similar:
                orig, dup = sorted([seen_story_id, doc.id], key=comparator)
                out = type1 if sim == -1.0 else type2
                out.write('{0} {1}\n'.format(orig, dup))


def main2(k):
    with nested(
        open('data.finn'),
        open('type3.dup', 'w'),
    ) as (train, type3):
        buckets = [defaultdict(list) for i in range(HASH_SIZE / k)]
        for doc in finn_parse(train):
            similar = get_similar(doc, buckets, k)
            for seen_story_id, sim in similar:
                orig, dup = sorted([seen_story_id, doc.id], key=comparator)
                type3.write('{0} {1}\n'.format(orig, dup))


if __name__ == '__main__':
    k = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_K
    # main(k)
    main2(k)
