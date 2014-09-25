import re

from contextlib import contextmanager
from collections import defaultdict


QRYS_FILE = './qrys.txt'
DOCS_FILE = './docs.txt'


def log(out_file, query_id, doc_id, val):
    """Log the result to the output file."""
    out_file.write('{} 0 {} 0 {} 0\n'.format(query_id, doc_id, val))


def tokenize(file_):
    """Tokenize line into id and tokens. Make words lowercase."""
    for line in file_:
        line_id, line_txt = line.split(' ', 1)
        line_txt = line_txt.lower()
        line_tokens = re.split('\W+', line_txt)  # split on non-word chars
        yield line_id, line_tokens

    file_.seek(0)  # reset file pointer


def dictify(tokens):
    """Turn tokens into a dict with words as keys and counts as values."""
    d = defaultdict(int)
    for token in tokens:
        d[token] += 1
    return d


@contextmanager
def read_std_files(out_file):
    """Open files and run similarity evaluation with the eval function."""
    qrys_file = open(QRYS_FILE, 'r')
    docs_file = open(DOCS_FILE, 'r')
    out_file = open(out_file, 'w')
    try:
        yield qrys_file, docs_file, out_file
    finally:
        qrys_file.close()
        docs_file.close()
        out_file.close()
