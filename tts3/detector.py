import math
import hashlib
import re

from contextlib import nested
from collections import defaultdict


DEFAULT_K = 24
STOP_WORDS = [word.rstrip('\n') for word in open('english.txt').readlines()]


def dictify(tokens):
    """Turn tokens into a dict with words as keys and counts as values."""
    dct = {}
    for token in tokens:
        dct.setdefault(token, 0)
        dct[token] += 1
    return dct


def hash_word(word):
    """Hashes a word into a binary sequence."""
    # get 16byte hash
    digest = hashlib.md5(word).digest()
    # convert to 4 byte chunks
    chunks = (digest[4 * i:4 * (i + 1)].encode('hex') for i in range(len(digest) / 4))
    # convert to  ints
    int_chunks = (int(chunk, 16) for chunk in chunks)
    # convert to one binary sequence
    return ''.join(bin(chunk).lstrip('0b') for chunk in int_chunks)


def hashsim(doc, k=DEFAULT_K):
    """Hashes a document using simhash."""
    # make array to store results
    hash_sum = [0] * 128
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
        yield story_id, dictify(tokens)


def simple_parse(file_):
    """Parses the file. Doesn't tokenize."""
    for line in file_:
        story_id, rest = line.strip().split(' ', 1)
        yield story_id, rest


def cosine(doc1, doc2):
    """Compute cosine similarity measure."""
    dw_dw = sum(tf_wq * tf_wq for tf_wq in doc2.itervalues())
    qw_qw = 0.0
    qw_dw = 0.0
    for word, tf_wq in doc1.iteritems():
        qw_qw += tf_wq * tf_wq
        if word in doc2:
            qw_dw += tf_wq * doc2[word]

    return qw_dw / math.sqrt(qw_qw * dw_dw)


def comparator(story_id):
    """Returns the int value from a story id."""
    return int(story_id.lstrip('t'))


def main1():
    with open('data.train') as train:
        seen = {}
        for story_id, text in simple_parse(train):
            if text in seen:
                # find which one was first
                orig, dup = sorted([seen[text], story_id], key=comparator)
                print('{0} {1}'.format(orig, dup))
            else:
                seen[text] = story_id


def main2():
    with nested(
        open('data.train'),
        open('type1.dup'),
        open('type2.dup'),
    ) as (train, type1, type2):
        buckets = [defaultdict(list) for i in range(5)]
        for story_id, tokens in parse(train):
            # compute the fingerprint hashes
            hashes = hashsim(tokens)
            similar = []
            for idx, hash_ in enumerate(hashes):
                bucket = buckets[idx]
                if hash_ in bucket:
                    # compare to everything in the same bucket
                    for seen_story_id, seen_tokens in bucket[hash_]:
                        sim = cosine(tokens, seen_tokens)
                        if sim > 0.8 and 1.0:
                            similar.append(seen_story_id)
                else:
                    bucket[hash_].append((story_id, tokens))

            for see_story_id in set(similar):
                orig, dup = sorted([seen_story_id, story_id], key=comparator)
                print('{0} {1}'.format(orig, dup))


if __name__ == '__main__':
    main2()
