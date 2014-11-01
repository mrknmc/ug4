import re


def parse(file_):
    """"""
    for line in file_:
        line = line.strip()
        story_id, rest = line.split(' ', 1)
        tokens = re.split(r'[\t\r\n\\~`!@#$%^&*()_-+=[]{}|:;"\'<>,.?/]+', rest)
        yield story_id, tokens


def simple_parse(file_):
    """Parses the file. Doesn't tokenize."""
    for line in file_:
        story_id, rest = line.strip().split(' ', 1)
        yield story_id, rest


def comparator(story_id):
    """Returns the int value from a story id."""
    return int(story_id.lstrip('t'))


def main():
    with open('data.train') as train:
        seen = {}
        for story_id, text in simple_parse(train):
            if text in seen:
                # find which one was first
                orig, dup = sorted([seen[text], story_id], key=comparator)
                print('{0} {1}'.format(orig, dup))
            else:
                seen[text] = story_id


if __name__ == '__main__':
    main()
