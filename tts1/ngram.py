"""
"""

import re

from collections import defaultdict
from itertools import chain
from tfidf import tfidf
from common import read_std_files, dictify, log

OUT_FILE = 'ngram.top'
TUNE_K = 2
NGRAM_SIZE = 4


def map_docs(docs_file):
    """Return total count of documents, tokens and inverted index counts."""
    word_map = defaultdict(int)
    doc_count = 0
    token_count = 0

    for _, doc_tokens in tokenize(docs_file):
        doc_count += 1  # count document
        token_count += len(doc_tokens)  # count tokens
        for token in set(doc_tokens):
            word_map[token] += 1  # increase inverted index count

    docs_file.seek(0)  # reset file pointer
    return doc_count, token_count, word_map


def ngramify(word, n):
    """Turns a word into a list of ngrams of length n."""
    return (word[i:i+n] for i in range(len(word) - n + 1))


def tokenize(file_):
    """Tokenize line into id and tokens. Make words lowercase."""
    for line in file_:
        line_id, line_txt = line.split(' ', 1)
        line_txt = line_txt.lower()
        line_tokens = re.split(r'\W+', line_txt)  # split on non-word chars
        ngrams = (ngramify(token, NGRAM_SIZE) for token in line_tokens)
        ngrammed_tokens = list(chain(*ngrams))
        yield line_id, ngrammed_tokens

    file_.seek(0)  # reset file pointer


def main():
    """For every query compute similarity to every document."""
    with read_std_files(OUT_FILE) as (qrys_file, docs_file, out_file):
        doc_count, token_count, word_map = map_docs(docs_file)
        avg_doc_len = token_count / float(doc_count)
        for query_id, query_tokens in tokenize(qrys_file):
            query_dct = dictify(query_tokens)
            for doc_id, doc_tokens in tokenize(docs_file):
                doc_len = len(doc_tokens)
                doc_dct = dictify(doc_tokens)
                similarity = tfidf(query_dct, doc_dct, doc_len, doc_count, avg_doc_len, word_map)
                log(out_file, query_id, doc_id, similarity)

if __name__ == '__main__':
    main()
