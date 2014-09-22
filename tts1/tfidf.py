import re
import sys
import math

from collections import defaultdict


QRYS_FILE = './qrys.txt'
DOCS_FILE = './docs.txt'
OUT_FILE = './tfidf.top'


def log(out_file, query_id, doc_id, val):
    """Log the result to the output file."""
    out_file.write('{} 0 {} 0 {:.4f} 0\n'.format(query_id, doc_id, val))


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

    for _, doc_tokens in tokenize(docs_file):
        doc_count += 1
        for token in set(doc_tokens):
            word_map[token] += 1

    docs_file.seek(0)
    return doc_count, word_map


def tfidf(qrys_file, docs_file, out_file):
    """Calculate the tfidf of a query and a document."""
    doc_count, word_map = map_docs(docs_file)
    for query_id, query_tokens in tokenize(qrys_file):
        # convert into a binary dict
        query_dct = dictify(query_tokens)

        for doc_id, doc_tokens in tokenize(docs_file):
            # convert into a binary dict
            doc_dct = dictify(doc_tokens)
            doc_len = len(doc_tokens)

            tfidf = 0
            for word, count in query_dct.iteritems():
                # skip if word not in document
                if word not in doc_dct:
                    continue
                tf = doc_dct[word] / float(doc_len)
                idf = math.log(doc_count / float(word_map[word]))
                tfidf += count * tf * idf

            log(out_file, query_id, doc_id, tfidf)


def main():
    qrys_file = open(QRYS_FILE, 'r')
    docs_file = open(DOCS_FILE, 'r')
    out_file = open(OUT_FILE, 'w')

    try:
        tfidf(qrys_file, docs_file, out_file)
    finally:
        qrys_file.close()
        docs_file.close()
        out_file.close()


if __name__ == '__main__':
    main()
