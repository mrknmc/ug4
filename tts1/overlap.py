import re
import sys

from collections import defaultdict


QRYS_FILE = './qrys.txt'
DOCS_FILE = './docs.txt'
OUT_FILE = './overlap.top'


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


def overlap(qrys_file, docs_file, out_file):
    """Calculate the overlap of a query and a document."""
    for query_id, query_tokens in tokenize(qrys_file):
        # convert into a binary dict
        query_dct = dictify(query_tokens, maxcount=1)

        for doc_id, doc_tokens in tokenize(docs_file):
            # convert into a binary dict
            doc_dct = dictify(doc_tokens, maxcount=1)

            # dot product one dictionary from another
            overlap = sum(count * doc_dct.get(word, 0) for word, count in query_dct.iteritems())
            out_file.write('{} 0 {} 0 {} 0\n'.format(query_id, doc_id, overlap))


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
