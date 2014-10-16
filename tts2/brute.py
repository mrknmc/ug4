

def log():
    pass


def tokenize(file_):
    """Tokenize line into id and tokens. Make words lowercase."""
    for line in file_:
        line_id, line_txt = line.split(' ', 1)
        line_txt = line_txt.strip().lower()
        line_tokens = re.split(r'\W+', line_txt)  # split on non-word chars
        if line_tokens[-1] == '':
            line_tokens = line_tokens[:-1]
        yield line_id, line_tokens


def similarity(tok1, tok2):
    pass


def main():
    with open('news.txt') as f:
        B = 1
        for i in range(1, A):
            if cosine(A, i) > cosine(A, B):
                B = i

def main():
    with open('news.txt') as f:
        cache = []
        for idx, (cur_id, cur_tokens) in enumerate(tokenize(f)):
            for prev_id, prev_tokens in cache:
#                 if similarity(cur_tokens, prev_tokens) > thresh:
#                     log()

#             # stop after 10,000
#             if idx == 10000:
#                 break


if __name__ == '__main__':
    main()
