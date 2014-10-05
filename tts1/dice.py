"""
"""

import re
import math

from Stemmer import Stemmer
from collections import defaultdict
from common import read_std_files, dictify, log, memoize

OUT_FILE = 'dice.top' 
TUNE_K = 5
STEMMER = Stemmer('english')


def map_docs(docs_file):
    """Return total count of documents, tokens and inverted index counts."""
    word_map = defaultdict(set)
    doc_count = 0
    token_count = 0

    for doc_id, doc_tokens in tokenize(docs_file):
        doc_count += 1  # count document
        token_count += len(doc_tokens)  # count tokens
        for token in doc_tokens:
            word_map[token].add(doc_id)  # add doc_id to set for every word

    docs_file.seek(0)  # reset file pointer
    return doc_count, token_count, word_map


def tokenize(file_):
    """Tokenize line into id and tokens. Make words lowercase."""
    for line in file_:
        line_id, line_txt = line.split(' ', 1)
        line_txt = line_txt.strip().lower()
        line_tokens = re.split(r'\W+', line_txt)  # split on non-word chars
        if line_tokens[-1] == '':
            line_tokens = line_tokens[:-1]  # drop the last word if ""
        stemmed_tokens = STEMMER.stemWords(line_tokens)
        yield line_id, stemmed_tokens

    file_.seek(0)  # reset file pointer


@memoize
def emim(word1, word2, word_map=None, doc_count=None):
    doc_set1, doc_set2 = word_map[word1], word_map[word2]
    n_a, n_b = len(doc_set1), len(doc_set2)
    n_ab = len(doc_set1 & doc_set2)
    if n_a == 0 or n_b == 0:
        return 0
    pre_log = doc_count * (float(n_ab) / (n_a * n_b))
    if pre_log == 0:
        return 0
    return n_ab * math.log(pre_log)


@memoize
def dice(word1, word2, word_map=None, doc_count=None):
    doc_set1, doc_set2 = word_map[word1], word_map[word2]
    n_a, n_b = len(doc_set1), len(doc_set2)
    n_ab = len(doc_set1 & doc_set2)
    if n_a == 0 or n_b == 0 or n_ab == 0:
        return 0
    return float(n_ab) / (n_a + n_b)


@memoize
def chi_squared(word1, word2, word_map=None, doc_count=None):
    doc_set1, doc_set2 = word_map[word1], word_map[word2]
    n_a, n_b = len(doc_set1), len(doc_set2)
    n_ab = len(doc_set1 & doc_set2)
    if n_a == 0 or n_b == 0 or n_ab == 0:
        return 0
    return math.pow(float(n_ab) - (1.0 / doc_count) * n_a * n_b, 2) / (n_a * n_b)


def sim(query_dct, doc_dct, doc_len, doc_count, avg_doc_len, word_map, k=TUNE_K):
    """Computes tf.idf for a given query and document."""
    emim_sum = 0.0
    for q_word, tf_wq in query_dct.iteritems():
        for d_word, tf_wd in doc_dct.iteritems():
            tf = tf_wd / (tf_wd + ((k * doc_len) / avg_doc_len))
            idf = math.log(doc_count / float(len(word_map[d_word])))
            dice_val = dice(q_word, d_word, word_map=word_map, doc_count=doc_count)
            emim_sum += tf_wq * tf * idf * dice_val

    return emim_sum


def main():
    """For every query compute similarity to every document."""
    with read_std_files(OUT_FILE) as (qrys_file, docs_file, out_file):
        doc_count, token_count, word_map = map_docs(docs_file)
        avg_doc_len = token_count / float(doc_count)
        for doc_id, doc_tokens in tokenize(docs_file):
            print(doc_id)
            doc_len = len(doc_tokens)
            doc_dct = dictify(doc_tokens)
            for query_id, query_tokens in tokenize(qrys_file):
                query_dct = dictify(query_tokens)
                similarity = sim(query_dct, doc_dct, doc_len, doc_count, avg_doc_len, word_map, k=TUNE_K)
                log(out_file, query_id, doc_id, similarity)

if __name__ == '__main__':
    main()
