"""
"""

import re
import math

from Stemmer import Stemmer
from collections import defaultdict
from common import read_std_files, dictify, log

OUT_FILE = 'best.top'
TUNE_K = 2


def map_docs(docs_file, stemmer):
    """Return total count of documents, tokens and inverted index counts."""
    word_map = defaultdict(int)
    doc_count = 0
    token_count = 0

    for _, doc_tokens in tokenize(docs_file, stemmer):
        doc_count += 1  # count document
        token_count += len(doc_tokens)  # count tokens
        for token in set(doc_tokens):
            word_map[token] += 1  # increase inverted index count

    docs_file.seek(0)  # reset file pointer
    return doc_count, token_count, word_map


def tfidf(query_dct, doc_dct, doc_len, doc_count, avg_doc_len, word_map):
    """Computes tf.idf for a given query and document."""
    tfidf_sum = 0
    for word, tf_wq in query_dct.iteritems():
        if word not in doc_dct:
            continue  # skip if word not in document

        tf_wd = doc_dct[word]
        tf = tf_wd / (tf_wd + ((TUNE_K * doc_len) / avg_doc_len))
        idf = math.log(doc_count / float(word_map[word]))
        tfidf_sum += tf_wq * tf * idf

    return tfidf_sum


def tokenize(file_, stemmer):
    """Tokenize line into id and tokens. Make words lowercase."""
    for line in file_:
        line_id, line_txt = line.split(' ', 1)
        line_txt = line_txt.lower()
        line_tokens = re.split(r'\W+', line_txt)  # split on non-word chars
        stemmed_tokens = stemmer.stemWords(line_tokens)
        yield line_id, stemmed_tokens

    file_.seek(0)  # reset file pointer


def main():
    """For every query compute similarity to every document."""
    with read_std_files(OUT_FILE) as (qrys_file, docs_file, out_file):
        stemmer = Stemmer('english')
        doc_count, token_count, word_map = map_docs(docs_file, stemmer)
        avg_doc_len = token_count / float(doc_count)
        for query_id, query_tokens in tokenize(qrys_file, stemmer):
            query_dct = dictify(query_tokens)
            for doc_id, doc_tokens in tokenize(docs_file, stemmer):
                doc_len = len(doc_tokens)
                doc_dct = dictify(doc_tokens)
                similarity = tfidf(query_dct, doc_dct, doc_len, doc_count, avg_doc_len, word_map)
                log(out_file, query_id, doc_id, similarity)

if __name__ == '__main__':
    main()

