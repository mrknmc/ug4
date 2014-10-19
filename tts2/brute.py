# import tqdm

DEFAULT_IDF = 13.6332


class Story(object):
    def __init__(self, id, vec, idfs):
        self.id, self.vec = id, vec
        tfidf_sum = 0.0
        for word, tf_wq in vec.iteritems():
            idf = idfs.get(word, DEFAULT_IDF)
            tfidf_sum += tf_wq * tf_wq * idf * idf
        self.tfidf = tfidf_sum


def similarity(story1, story2, idfs):
    """Computes the similarity of two stories using cosines."""
    qw_dw = tfidf(story1, story2, idfs)
    qw_qw = story1.tfidf
    dw_dw = story2.tfidf
    return qw_dw / pow(qw_qw * dw_dw, 0.5)


def tfidf(story1, story2, idfs):
    """Computes tf.idf for a given query and document."""
    tfidf_sum = 0.0
    for word, tf_wq in story1.vec.iteritems():
        tf_wd = story2.vec.get(word, 0)
        idf = idfs.get(word, DEFAULT_IDF)
        tfidf_sum += tf_wq * tf_wd * idf * idf
    return tfidf_sum


def parse_news(file_, idfs):
    """Tokenize line into id and lowercase token vector."""
    for line in file_:
        story_id, line_txt = line.split(' ', 1)
        tokens = line_txt.strip().lower().split()
        yield Story(int(story_id), dictify(tokens), idfs)


def parse_idfs(news_idf):
    """Make a dict from news.idf."""
    idfs = {}
    for line in news_idf:
        idf, word = line.split()
        idfs[word] = float(idf)
    return idfs


def log(out_file, story1_id, story2_id):
    """Log the result to the output file."""
    out_file.write('{0} {1}\n'.format(story1_id, story2_id))


def dictify(tokens):
    """Turn tokens into a dict with words as keys and counts as values."""
    dct = {}
    for token in tokens:
        dct.setdefault(token, 0)
        dct[token] += 1
    return dct


def main(thresh=0.2, stop=1000):
    try:
        news_txt = open('news.txt')
        news_idf = open('news.idf')
        out_file = open('pairs.out', 'w')

        idfs = parse_idfs(news_idf)  # create idf map
        stories = parse_news(news_txt, idfs)  # story generator
        cache = [stories.next()]  # put first story in the cache

        # for every story starting from #2 and stopping at #10,000
        # for idx, cur_story in tqdm.tqdm(enumerate(stories, start=2), total=stop):
        for idx, cur_story in enumerate(stories, start=2):
            # similarity function
            sim = lambda story: similarity(cur_story, story, idfs)
            # compare to every story in the cache
            sims = ((sim(prev_story), prev_story) for prev_story in cache)
            # get story with max similarity
            max_sim, max_story = max(sims, key=lambda x: x[0])
            # output ids if similarity above thresh
            if max_sim > thresh:
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
