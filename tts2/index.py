# import tqdm


DEFAULT_IDF = 13.6332


class Story(object):
    def __init__(self, id, vec, idfs):
        self.id, self.vec = id, vec
        tfidf_sum = 0.0
        for word, tf_wq in vec.iteritems():
            idf = idfs.get(word, DEFAULT_IDF)
            tfidf_sum += tf_wq * tf_wq * idf * idf
        self.tfidf_sqrt = pow(tfidf_sum, 0.5)


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


def max_sim(query, index, idfs, tfidfs):
    """Finds most similar document for a given query document."""
    # create dict for every doc with a smaller id
    scores = dict((i + 1, 0.0) for i in xrange(query.id - 1))
    # for every term in the story
    for word, tf_wq in query.vec.iteritems():
        idf = idfs.get(word, DEFAULT_IDF)
        if word in index:
            # increase score for documents
            for doc_id, tf_wd in index[word]:
                scores[doc_id] += tf_wq * tf_wd * idf * idf

    # find the most similar doc
    max_sim, max_id = 0.0, 1
    for doc_id, score in scores.iteritems():
        cosine = score / (query.tfidf_sqrt * tfidfs[doc_id - 1])
        if cosine > max_sim:
            max_sim = cosine
            max_id = doc_id

    return max_id, max_sim


def update_index(index, story):
    """Updates the index with the story."""
    for word, count in story.vec.iteritems():
        lst = index.setdefault(word, [])
        lst.append((story.id, count))


def main(thresh=0.2, stop=10000):
    try:
        news_txt = open('news.txt')
        news_idf = open('news.idf')
        out_file = open('pairs.out', 'w')

        idfs = parse_idfs(news_idf)  # create idf map
        stories = parse_news(news_txt, idfs)  # story generator
        tfidfs = []
        index = {}
        first_story = stories.next()
        update_index(index, first_story)  # update index with first story
        tfidfs.append(first_story.tfidf_sqrt)
        # for every story starting from #2 and stopping at #10,000
        # for idx, cur_story in tqdm.tqdm(enumerate(stories, start=2), total=stop):
        for idx, cur_story in enumerate(stories, start=2):
            # get story with max similarity
            max_id, sim = max_sim(cur_story, index, idfs, tfidfs)
            # output ids if similarity above thresh
            if sim > thresh:
                log(out_file, cur_story.id, max_id)
            # update index with story
            update_index(index, cur_story)
            # update tfidf map
            tfidfs.append(cur_story.tfidf_sqrt)

            if idx == stop:
                break

    finally:
        news_txt.close()
        news_idf.close()
        out_file.close()


if __name__ == '__main__':
    main()
