import tqdm


DEFAULT_IDF = 13.6332


class Story(object):
    def __init__(self, id, vec):
        self.id, self.vec = id, vec


def parse_news(file_):
    """Tokenize line into id and lowercase token vector."""
    for line in file_:
        story_id, line_txt = line.split(' ', 1)
        line_txt = line_txt.strip().lower()
        tokens = line_txt.split(' ')
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
        dct.setdefault(token, 0)
        dct[token] += 1
    return dct


def max_sim(query, index, idfs=None, tfidfs=None):
    """Finds most similar document for a given query document."""
    # create dict for every doc with a smaller id
    scores = dict((i + 1, 0.0) for i in xrange(query.id - 1))
    qw_qw = 0.0
    # for every term in the story
    for word, tf_wq in query.vec.iteritems():
        idf = idfs.get(word, DEFAULT_IDF)
        # increase query terms sum
        qw_qw += tf_wq * tf_wq * idf
        if word in index:
            # increase score for documents
            for doc_id, tf_wd in index[word]:
                scores[doc_id] += tf_wq * tf_wd * idf

    sim_func = lambda s: s[1] / (pow(qw_qw, 0.5) * pow(tfidfs[s[0]], 0.5))
    return max(scores.iteritems(), key=sim_func)


def tfidf(story1, story2, idfs=None):
    """Computes tf.idf for a given query and document."""
    tfidf_sum = 0.0
    for word, tf_wq in story1.vec.iteritems():
        tf_wd = story2.vec.get(word, 0)
        tfidf_sum += tf_wq * tf_wd * idfs.get(word, DEFAULT_IDF)
    return tfidf_sum


def update_index(index, story):
    """Updates the index with the story."""
    for word, count in story.vec.iteritems():
        lst = index.setdefault(word, [])
        lst.append((story.id, count))


def main(thresh=0.2, stop=10000):
    try:
        news_txt = open('news.txt')
        news_idf = open('news.idf')
        out_file = open('pairs2.out', 'w')

        stories = parse_news(news_txt)  # story generator
        idfs = parse_idfs(news_idf)  # create idf map
        tfidfs = {}
        index = {}
        first_story = stories.next()
        update_index(index, first_story)  # update index with first story
        tfidfs[first_story.id] = tfidf(first_story, first_story, idfs=idfs)
        # for every story starting from #2 and stopping at #10,000
        for idx, cur_story in tqdm.tqdm(enumerate(stories, start=2), total=stop):
            # get story with max similarity
            sim, max_id = max_sim(cur_story, index, idfs=idfs, tfidfs=tfidfs)
            # output ids if similarity above thresh
            if sim > thresh:
                log(out_file, cur_story.id, max_id)
            # update index with story
            update_index(index, cur_story)
            # update tfidf map
            tfidfs[cur_story.id] = tfidf(cur_story, cur_story, idfs=idfs)

            if idx == stop:
                break
    finally:
        news_txt.close()
        news_idf.close()
        out_file.close()


if __name__ == '__main__':
    main()
