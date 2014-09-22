import re
import sys
import itertools

from collections import defaultdict


QRYS_FILE = './qrys.txt'
DOCS_FILE = './docs.txt'
OUT_FILE = './overlap.top'


def tokenize(line):
    """Tokenize line into id and tokens."""
    line_id, line_txt = line.split(' ', 1)
    line_txt = line_txt.lower()
    line_tokens = re.split('\W+', line_txt)
    return line_id, line_tokens


def dictify(tokens, maxcount=sys.maxint):
    """Turn tokens into a dict with words as keys and counts as values."""
    d = defaultdict(int)
    for token in tokens:
        d[token] = min(d[token] + 1, maxcount)
    return d


def subtract(dct1, dct2):
    """Subtract one dictionary from another."""
    return dict((key, val - dct2.get(key, 0)) for key, val in dct1.iteritems())


def overlap(qrys_file, docs_file, out_file):
    """Calculate the overlap of a query and a document."""
    for query in qrys_file:
        # split into id and tokens
        query_id, query_tokens = tokenize(query)
        # convert into a binary dict
        query_dct = dictify(query_tokens, maxcount=1)

        for doc in docs_file:
            # split into id and tokens
            doc_id, doc_tokens = tokenize(doc)
            # convert into a binary dict
            doc_dct = dictify(doc_tokens, maxcount=1)

            diff_dct = subtract(query_dct, doc_dct)
            doc_overlap = sum(diff_dct.itervalues())

            out_file.write('{} 0 {} 0 {} 0\n'.format(query_id, doc_id, doc_overlap))


def main():
    qrys_file = open(QRYS_FILE, 'r')
    docs_file = open(DOCS_FILE, 'r')
    out_file = open(OUT_FILE, 'w')

    try:
        overlap(qrys_file, docs_file, out_file)
    finally:
        qrys_file.close()
        docs_file.close()
        out_file.close()


if __name__ == '__main__':
    main()
