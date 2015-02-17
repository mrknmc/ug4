
from math import log
from argparse import ArgumentParser


def cache(file_, lines, words):
    """
    Simulates a set-associative cache.
        :param file_: Tracefile used for simulation.
        :param lines: Number of lines in a cache.
        :param words: Number of words in a block.
        :returns:
    """
    cache = {}
    total = {'R': 0, 'W': 0}
    misses = {'R': 0, 'W': 0}
    index_size = int(log(lines, 2))

    for cpu, op, index, tag in parse(file_, index_size):
        total[op] += 1

        if index not in cache:
            # not in cache - add it
            misses[op] += 1
            cache[index] = tag
        else:
            # something in cache
            if tag == cache[index]:
                # it is the same address => hit
                pass
            else:
                # it is a different address => evicted
                cache[index] = tag

    return total, misses


def parse(file_, index_size):
    """
    Generator that parses a given file.
        :param file_: file to parse.
        :returns:
    """
    index_mask = pow(2, index_size) - 1

    for line in file_:
        if line.startswith('v'):
            # switch on line-by-line explanation
            pass
        elif line.startswith('p'):
            # print out cache contents
            pass
        elif line.startswith('h'):
            # print out hit rate
            pass
        elif line.startswith('i'):
            # print out number of invalidations
            pass
        elif line.startswith('P'):
            # processor doing things
            cpu, op, addr = line.split()
            addr = int(addr)
            index = addr & index_mask
            tag = addr >> index_size
            yield cpu, op, tag, index

    file_.seek(0)  # reset file pointer


def main():
    parser = ArgumentParser(description='Run a cache simulator on a given trace file.')
    parser.add_argument(
        'filename',
        metavar='tracefile',
        type=str,
        help='Path of the file to process.',
    )
    parser.add_argument(
        '--lines',
        type=int,
        default=1024,
        help='Number of lines in a cache.'
    )
    parser.add_argument(
        '--words',
        type=int,
        default=4,
        help='Number of words in a line.'
    )
    args = vars(parser.parse_args())
    with open(args['filename']) as file_:
        cache(file_, args['lines'], args['words'])
        # total_sum = sum(total.itervalues())
        # misses_sum = sum(misses.itervalues())
        # print('Total Miss Rate: {:.4%}'.format(misses_sum / float(total_sum)))
        # print('Read Miss Rate: {:.4%}'.format(misses['R'] / float(total['R'])))
        # print('Write Miss Rate: {:.4%}'.format(misses['W'] / float(total['W'])))


if __name__ == '__main__':
    main()
