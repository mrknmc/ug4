import math

from collections import defaultdict
from common import tokenize, dictify, log, read_std_files

TUNE_K = 2
OUT_FILE = 'ntfidf.top'


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


def tfidf(query_dct, doc_dct, doc_len, doc_count, avg_doc_len, word_map, k=TUNE_K):
    """Computes tf.idf for a given query and document."""
    tfidf_sum = 0
    tf_run = []
    for word, tf_wq in query_dct.iteritems():
        if word not in doc_dct:
            continue  # skip if word not in document

        tf_wd = doc_dct[word]
        tf = tf_wd / (tf_wd + ((k * doc_len) / avg_doc_len))
        tf_run.append(tf)

    max_tf = max(tf_run) if tf_run else 0
    for word, tf_wq in query_dct.iteritems():
        if word not in doc_dct:
            continue

        tf_wd = doc_dct[word]
        tf = tf_wd / (tf_wd + ((k * doc_len) / avg_doc_len))
        ntf = 0.9 + (1 - 0.9) * (tf / max_tf)
        idf = math.log(doc_count / float(word_map[word]))
        tfidf_sum += tf_wq * ntf * idf

    return tfidf_sum


def main():
    """For every query compute similarity to every document."""
    with read_std_files(OUT_FILE) as (qrys_file, docs_file, out_file):
        doc_count, token_count, word_map = map_docs(docs_file)
        avg_doc_len = token_count / float(doc_count)
        for doc_id, doc_tokens in tokenize(docs_file):
            doc_len = len(doc_tokens)
            doc_dct = dictify(doc_tokens)
            for query_id, query_tokens in tokenize(qrys_file):
                query_dct = dictify(query_tokens)
                similarity = tfidf(query_dct, doc_dct, doc_len, doc_count, avg_doc_len, word_map)
                log(out_file, query_id, doc_id, similarity)


if __name__ == '__main__':
    main()