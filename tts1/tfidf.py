import evaluate
import math

from collections import defaultdict
from contextlib import contextmanager

TUNE_K = 2


def map_docs(docs_file):
    """Return total count of documents, tokens and inverted index counts."""
    word_map = defaultdict(int)
    doc_count = 0
    token_count = 0

    for _, doc_tokens in evaluate.tokenize(docs_file):
        doc_count += 1  # count document
        token_count += len(doc_tokens)  # count tokens
        for token in set(doc_tokens):
            word_map[token] += 1  # increase inverted index count

    docs_file.seek(0)  # reset file pointer
    return doc_count, token_count, word_map


@contextmanager
def tfidf(docs_file):
    doc_count, token_count, word_map = map_docs(docs_file)
    avg_doc_len = token_count / float(doc_count)

    def tfidf_inner(query_dct, doc_dct):
        doc_len = float(sum(doc_dct.itervalues()))  # count document length

        tfidf_sum = 0
        for word, tf_wq in query_dct.iteritems():
            if word not in doc_dct:
                continue  # skip if word not in document

            tf_wd = doc_dct[word]
            tf = tf_wd / (tf_wd + ((TUNE_K * doc_len) / avg_doc_len))
            idf = math.log(doc_count / float(word_map[word]))
            tfidf_sum += tf_wq * tf * idf

        return tfidf_sum
    yield tfidf_inner


if __name__ == '__main__':
    evaluate.main(tfidf, 'tfidf.top')
