import re

from collections import defaultdict


class Story(object):
    def __init__(self, id, vec):
        self.id, self.vec = id, vec

    def __hash__(self):
        return hash(self.id)


def parse_news(file_):
    """Tokenize line into id and lowercase token vector."""
    for line in file_:
        story_id, line_txt = line.split(' ', 1)
        line_txt = line_txt.strip().lower()
        tokens = re.split(r'\W+', line_txt)  # split on non-word chars
        if tokens[-1] == '':
            tokens = tokens[:-1]  # remove empty if sentence ends with punct
        yield Story(id=story_id, vec=dictify(tokens))


def parse_idfs(news_idf):
    """Make a dict from news.idf."""
    idfs = {}
    for line in news_idf:
        idf, word = line.split()
        idfs[word] = float(idf)
    return idfs


def log(out_file, story1_id, story2_id):
    """Log the result to the output file."""
    out_file.write('{0},{1}\n'.format(story1_id, story2_id))


def dictify(tokens):
    """Turn tokens into a dict with words as keys and counts as values."""
    dct = defaultdict(int)
    for token in tokens:
        dct[token] += 1
    return dct


def memoize(obj):
    """Caches function results based on args but not kwargs."""
    cache = obj.cache = {}

    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer
