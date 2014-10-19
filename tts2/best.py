# import tqdm


DEFAULT_IDF = 13.6332
DEFAULT_K = 100


def bin_search(lst, value):
    """"""
    # adapted from http://rosettacode.org/wiki/Binary_search#Python
    low = 0
    high = len(lst) - 1
    while low <= high:
        mid = (low + high) // 2
        if lst[mid] > value:
            high = mid - 1
        elif lst[mid] < value:
            low = mid + 1
        else:
            return mid
    return low


class List(object):
    def __init__(self, k=DEFAULT_K):
        self._ranked = []
        self.k = k
        self._inv_list = []

    def append(self, story, sim):
        """"""
        # add to normal inv list
        self._inv_list.append((story.id, sim))
        # add to ranked if ranked well
        place = bin_search(self._ranked, sim)
        # place if place for it
        if place <= self.k:
            self._ranked.insert(place, (story.id, sim))
            # delete last one if oversized
            if len(self._ranked) > self.k:
                del(self._ranked[-1])

    def __iter__(self):
        if len(self._inv_list) < 100:
            return self.inv_list()
        else:
            return self.ranked()

    def ranked(self):
        for tup in self._ranked:
            yield tup

    def inv_list(self):
        for tup in self._inv_list:
            yield tup


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
    scores = {}
    # for every term in the story
    for word, tf_wq in query.vec.iteritems():
        idf = idfs.get(word, DEFAULT_IDF)
        if word in index:
            # increase score for documents
            for doc_id, tf_wd in index[word]:
                tfidf_val = tf_wq * tf_wd * idf * idf
                if doc_id in scores:
                    scores[doc_id] += tfidf_val
                else:
                    scores[doc_id] = tfidf_val

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
        lst = index.setdefault(word, List())
        lst.append(story, count)


def tfidf(story1, story2, idfs):
    """Computes tf.idf for a given query and document."""
    tfidf_sum = 0.0
    for word, tf_wq in story1.vec.iteritems():
        tf_wd = story2.vec.get(word, 0)
        tfidf_sum += tf_wq * tf_wd * pow(idfs.get(word, DEFAULT_IDF), 2)
    return tfidf_sum


def main(thresh=0.2, stop=1000):
    try:
        news_txt = open('news.txt')
        news_idf = open('news.idf')
        out_file = open('pairs3.out', 'w')

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
