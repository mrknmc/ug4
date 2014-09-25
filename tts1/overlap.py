from common import tokenize, dictify, log, read_std_files

OUT_FILE = 'overlap.top'


def overlap(query_dct, doc_dct):
    """Count number of words that are in both query and document."""
    return sum(1 for word in query_dct if word in doc_dct)


def main():
    """For every query compute similarity to every document."""
    with read_std_files(OUT_FILE) as (qrys_file, docs_file, out_file):
        for query_id, query_tokens in tokenize(qrys_file):
            query_dct = dictify(query_tokens)
            for doc_id, doc_tokens in tokenize(docs_file):
                doc_dct = dictify(doc_tokens)
                similarity = overlap(query_dct, doc_dct)
                log(out_file, query_id, doc_id, similarity)


if __name__ == '__main__':
    main()
