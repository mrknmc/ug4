import evaluate
from contextlib import contextmanager


@contextmanager
def overlap(docs_file):
    def olap(query_dct, doc_dct):
        """Count number of words that are in both query and document."""
        return sum(1 for word in query_dct if word in doc_dct)
    yield olap


if __name__ == '__main__':
    evaluate.main(overlap, 'overlap.top')
