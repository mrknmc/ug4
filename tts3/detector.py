import math
import hashlib
import re

from contextlib import nested
from collections import defaultdict


DEFAULT_K = 24
HASH_SIZE = 128
STOP_WORDS = [word.rstrip('\n') for word in open('english.txt')]


class Doc(dict):
    def __init__(self, id_, tokens):
        self.id = id_
        for token in tokens:
            self.setdefault(token, 0)
            self[token] += 1.0
        self.dist = math.sqrt(sum(freq * float(freq) for freq in self.itervalues()))


def hash_word(word):
    """Hashes a word into a binary sequence."""
    # get 16-byte hash
    digest = hashlib.md5(word).digest()
    # convert to 4-byte chunks
    chunks = (digest[4 * i:4 * (i + 1)].encode('hex') for i in range(len(digest) / 4))
    # convert to ints
    int_chunks = (int(chunk, 16) for chunk in chunks)
    # convert to one binary sequence
    return ''.join(bin(chunk).lstrip('0b') for chunk in int_chunks)


def hashsim(doc, k=DEFAULT_K):
    """Hashes a document using simhash."""
    # make array to store results
    hash_sum = [0] * HASH_SIZE
    for word, freq in doc.iteritems():
        # compute hash for every word
        word_hash = hash_word(word)
        for idx, char in enumerate(word_hash):
            # sum char vals in each column
            hash_sum[idx] += freq if char == '1' else -freq
    # combine into a binary string
    fingerprint = ''.join('1' if hsum > 0 else '0' for hsum in hash_sum)
    return (fingerprint[k * i:k * (i + 1)] for i in range(len(fingerprint) / k))


def parse(file_):
    """Parses the file, tokenizes and removes stop words."""
    for line in file_:
        story_id, rest = line.strip().lower().split(' ', 1)
        # tokenize
        tokens = re.split(r'[\t\r\n\\~`!@#$%^&*\(\)_\-+=\[\]\{\}|:;"\'<>,.?/]+', rest)
        # remove stop words
        tokens = [token for token in tokens if token not in STOP_WORDS]
        yield Doc(story_id, tokens)


def cosine(doc1, doc2):
    """Compute cosine similarity measure."""
    qw_dw = 0.0
    for word, tf_wq in doc1.iteritems():
        if word in doc2:
            qw_dw += tf_wq * doc2[word]
    return qw_dw / (doc1.dist * doc2.dist)


def comparator(story_id):
    """Returns the int value from a story id."""
    return int(story_id.lstrip('t'))


def get_similar(doc, buckets):
    """Returns document ids that are in the same bucket and are similar."""
    # compute the fingerprint hashes
    similar = set()
    hashes = hashsim(doc)
    for idx, hash_ in enumerate(hashes):
        bucket = buckets[idx]
        if hash_ in bucket:
            for seen_doc in bucket[hash_]:
                if seen_doc.id not in similar:
                    sim = cosine(doc, seen_doc)
                    if sim > 0.8:
                        similar.add((seen_doc.id, sim))
        else:
            bucket[hash_].append(doc)
    return similar


def main():
    with nested(
        open('data.train'),
        open('type1.dup', 'w'),
        open('type2.dup', 'w'),
    ) as (train, type1, type2):
        buckets = [defaultdict(list) for i in range(HASH_SIZE / DEFAULT_K)]
        for doc in parse(train):
            similar = get_similar(doc, buckets)
            for seen_story_id, sim in similar:
                orig, dup = sorted([seen_story_id, doc.id], key=comparator)
                print orig, dup, sim
                print sim < 1.0
                print type(sim)
                out = type1 if sim == 1.0 else type2
                out.write('{0} {1}\n'.format(orig, dup))


if __name__ == '__main__':
    main()
