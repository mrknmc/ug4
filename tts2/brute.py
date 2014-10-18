import tqdm

DEFAULT_IDF = 13.6332


class Story(object):
    def __init__(self, id, vec):
        self.id, self.vec = id, vec

    def __hash__(self):
        return hash(self.id)


def memoize(obj):
    """Caches function results based on args but not kwargs."""
    cache = obj.cache = {}

    def memoizer(*args, **kwargs):
        if args not in cache:
            cache[args] = obj(*args, **kwargs)
        return cache[args]
    return memoizer


def similarity(story1, story2, idfs=None):
    """Computes the similarity of two stories using cosines."""
    qw_dw = tfidf(story1, story2, idfs=idfs)
    qw_qw = tfidf(story1, story1, idfs=idfs)
    dw_dw = tfidf(story2, story2, idfs=idfs)
    return qw_dw / (pow(qw_qw, 0.5) * pow(dw_dw, 0.5))


@memoize
def tfidf(story1, story2, idfs=None):
    """Computes tf.idf for a given query and document."""
    tfidf_sum = 0.0
    for word, tf_wq in story1.vec.iteritems():
        if word not in story2.vec:
            continue  # skip if word not in document

        tfidf_sum += tf_wq * story2.vec[word] * idfs.get(word, DEFAULT_IDF)

    return tfidf_sum


def parse_news(file_):
    """Tokenize line into id and lowercase token vector."""
    for line in file_:
        story_id, line_txt = line.split(' ', 1)
        line_txt = line_txt.strip().lower()
        tokens = line_txt.split(' ')
        # tokens = re.split(r'\W+', line_txt)  # split on non-word chars
        if tokens[-1] == '':
            tokens = tokens[:-1]  # remove empty if sentence ends with punct
        yield Story(id=int(story_id), vec=dictify(tokens))


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
    dct = {}
    for token in tokens:
        if token in dct:
            dct[token] += 1
        else:
            dct[token] = 1
    return dct


def main(thresh=0.2, stop=10000):
    try:
        news_txt = open('news.txt')
        news_idf = open('news.idf')
        out_file = open('pairs.out', 'w')
        # story generator
        stories = parse_news(news_txt)
        # create idf map
        idfs = parse_idfs(news_idf)
        # put first story in the cache
        cache = [stories.next()]
        # for every story starting from #2 and stopping at #10,000
        for idx, cur_story in tqdm.tqdm(enumerate(stories, start=2), total=stop):
            # similarity function
            sim = lambda story: similarity(cur_story, story, idfs=idfs)
            # compare to every story in the cache
            sims = ((sim(prev_story), prev_story) for prev_story in cache)
            # get story with max similarity
            sim, max_story = max(sims, key=lambda x: x[0])
            # output ids if similarity above thresh
            if sim > thresh:
                log(out_file, cur_story.id, max_story.id)
            # add the story to the cache after done
            cache.append(cur_story)

            if idx == stop:
                break
    finally:
        news_txt.close()
        news_idf.close()
        out_file.close()


if __name__ == '__main__':
    main()
