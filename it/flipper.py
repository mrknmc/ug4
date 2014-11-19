import random
import sys


def noise(stream, f=0.4):
    """Adds noise to a stream with flip probability f."""
    while 1:
        num = stream.read(1)
        if num in ['\n', '']:
            break
        num = int(num)
        if random.random() < f:
            yield str(1 - num)
        else:
            yield str(num)


if __name__ == '__main__':
    for char in noise(sys.stdin, f=0.4):
        sys.stdout.write(char)
