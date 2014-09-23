import re
import sys
import math

from collections import defaultdict


QRYS_FILE = './qrys.txt'
DOCS_FILE = './docs.txt'
OUT_FILE = './tfidf.top'
TUNE_K = 2


class TfIdf(object):

    def __init__(self, docs_file):
        doc_count, token_count, word_map = map_docs(docs_file)
        self.avg_doc_len = token_count / float(doc_count)
        self.doc_count = doc_count
        self.word_map = word_map

    def __enter__(self):
        def tfidf(query_dct, doc_dct):
            doc_len = float(sum(doc_dct.itervalues()))
            print(doc_len)

            tfidf_sum = 0
            for word, tf_wq in query_dct.iteritems():
                # skip if word not in document
                if word not in doc_dct:
                    continue

                tf_wd = doc_dct[word]

                tf = tf_wd / (tf_wd + ((TUNE_K * doc_len) / self.avg_doc_len))
                idf = math.log(self.doc_count / float(self.word_map[word]))

                tfidf_sum += tf_wq * tf * idf
            return tfidf_sum
        return tfidf

    def __exit__(self, exc_type, exc_value, traceback):
        pass


def log(out_file, query_id, doc_id, val):
    """Log the result to the output file."""
    out_file.write('{} 0 {} 0 {} 0\n'.format(query_id, doc_id, val))


def tokenize(file_):
    """Tokenize line into id and tokens."""
    for line in file_:
        line_id, line_txt = line.split(' ', 1)
        line_txt = line_txt.lower()
        line_tokens = re.split('\W+', line_txt)
        yield line_id, line_tokens

    file_.seek(0)


def dictify(tokens, maxcount=sys.maxint):
    """Turn tokens into a dict with words as keys and counts as values."""
    d = defaultdict(int)
    for token in tokens:
        d[token] = min(d[token] + 1, maxcount)
    return d


def map_docs(docs_file):
    """Return count of documents and inverted index."""
    word_map = defaultdict(int)
    doc_count = 0
    token_count = 0

    for _, doc_tokens in tokenize(docs_file):
        doc_count += 1
        token_count += len(doc_tokens)
        for token in set(doc_tokens):
            word_map[token] += 1

    docs_file.seek(0)
    return doc_count, token_count, word_map


def worker(qrys_file, docs_file, out_file, val_func):
    for query_id, query_tokens in tokenize(qrys_file):
        # convert into a binary dict
        query_dct = dictify(query_tokens, maxcount=1)

        for doc_id, doc_tokens in tokenize(docs_file):
            # convert into a binary dict
            doc_dct = dictify(doc_tokens, maxcount=1)

            value = val_func(query_dct, doc_dct)
            log(out_file, query_id, doc_id, value)


def main():
    qrys_file = open(QRYS_FILE, 'r')
    docs_file = open(DOCS_FILE, 'r')
    out_file = open(OUT_FILE, 'w')

    try:
        with TfIdf(docs_file) as val_func:
            worker(qrys_file, docs_file, out_file, val_func)
    finally:
        qrys_file.close()
        docs_file.close()
        out_file.close()


if __name__ == '__main__':
    main()
