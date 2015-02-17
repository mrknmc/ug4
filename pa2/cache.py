import math

from collections import namedtuple
from argparse import ArgumentParser


Instruction = namedtuple('Instruction', ['cpu', 'op', 'index', 'tag', 'address'])

FORMAT = (
    'A {op} by processor {cpu} to word {addr} looked'
    ' for tag {tag} in cache line {index},'
    ' was found in state {state} in this cache.'
)

EXTENDED_FORMAT = (
    'A {op} by processor {cpu} to word {addr} looked'
    ' for tag {tag} in cache line {index},'
    ' was found in state {state} in this cache'
    ' and found in states {states} in the caches of {cpus}.'
)

MSI_LOCAL_STATES = {
    'M': {
        'R': {
            'hit': 'M',
            'miss': 'S',
        },
        'W': {
            'hit': 'M',
            # change to exclusive in MESI but probs stay same here
            'miss': 'M',
        },
    },
    'S': {
        'R': {
            'hit': 'S',
            'miss': 'S',
        },
        'W': {
            'miss': 'M',
            'hit': 'M',
        }
    },
    'I': {
        'R': {'miss': 'S'},
        'W': {'miss': 'M'},
    },
}

MSI_REMOTE_STATES = {
    'M': {
        'R': {'miss': 'S'},
        'W': {'miss': 'I'},
    },
    'S': {
        'R': {
            'miss': 'S',
            'hit': 'S',
        },
        'W': {'miss': 'I'},
    },
}

MESI_LOCAL_STATES = {
    'M': {
        'R': {'hit': 'M'},
        'W': {'hit': 'M'},
    },
    'E': {
        'R': {'hit': 'E'},
        'W': {'miss': 'M'},
    },
    'S': {
        'R': {'hit': 'S'},
        'W': {'miss': 'M'},
    },
    'I': {
        # either S or M
        'R': {'miss': ''},
        'W': {'miss': 'M'},
    },
}

MESI_REMOTE_STATES = {
    'M': {
        'R': {'miss': 'S'},
        'W': {'miss': 'I'},
    },
    'E': {
        'R': {'miss': 'S'},
        'W': {'miss': 'I'},
    },
    'S': {
        'R': {'miss': 'S'},
        'W': {'miss': 'I'},
    },
}


def log(instr, states):
    """Log to standard output."""
    format = EXTENDED_FORMAT if len(states) > 1 else FORMAT
    extra = {
        'op': instr.op,
        'cpu': 'P{}'.format(instr.cpu),
        'addr': instr.address,
        'tag': instr.tag,
        'index': instr.index,
        'state': states[instr.cpu],
        'states': ', '.join(state for (cpu, state) in states.items()),
        'cpus': ', '.join('P{}'.format(cpu) for (cpu, state) in states.items()),
    }
    print(format.format(**extra))


def make_instruction(line, index_size):
    """
    Parse an instruction.
        :param line: Line to parse.
        :param index_size: Size of index.
        :returns: CPU id, operator, index, tag, and address.
    """
    cpu, op, addr = line.split()
    addr = int(addr)
    cpu = int(cpu.lstrip('P'))  # strip P from CPU number
    # bitmask out index and tag
    index_mask = pow(2, index_size) - 1
    index = addr & index_mask
    tag = addr >> index_size
    return Instruction(cpu, op, index, tag, addr)


def has_line(cache, instr):
    """
    Return true if cache has the line needed by the instruction
        :param c: Cache we check.
        :param instr: Instruction we check.
        :returns: True if the cache contains the line in valid state.
    """
    return (
        instr.index in cache and
        cache[instr.index]['tag'] == instr.tag and
        cache[instr.index]['state'] != 'I'
    )


def process_instruction(cache, instr):
    """
    Process an instruction.
        :param op: Operation to execute.
        :param instr: Instruction to process.
        :returns: 'hit' or 'miss'.
    """
    # not in cache => miss and replace
    if instr.index not in cache:
        return 'miss'

    # different tag => miss and replace
    if cache[instr.index]['tag'] != instr.tag:
        return 'miss'

    # invalid state is a miss and write in shared is a miss
    line_state = cache[instr.index]['state']
    if (line_state == 'S' and instr.op == 'W') or line_state == 'I':
        return 'miss'

    # same tag and not invalid state is a hit
    return 'hit'


def remote_transition(cache, instr, event):
    """
    Transition the cache according to a local event.
        :param cache: Cache to transition.
        :param instr: Instruction that was processed.
        :param event: Hit or miss.
        :returns: Tuple of old and new state.
    """
    states = MSI_REMOTE_STATES
    old_state = cache[instr.index]['state']
    new_state = states[old_state][instr.op][event]
    cache[instr.index]['state'] = new_state
    return old_state


def local_transition(cache, instr, event):
    """
    Transition the cache according to a local event.
        :param cache: Cache to transition.
        :param instr: Instruction that was processed.
        :param event: Hit or miss.
        :returns: Tuple of old and new state.
    """
    states = MSI_LOCAL_STATES
    # TODO: is it ok to assume Invalid if nothing in cache?
    old_state = cache[instr.index]['state'] if instr.index in cache else 'I'
    new_state = states[old_state][instr.op][event]
    # different or same line, replace anyway
    cache[instr.index] = {'tag': instr.tag, 'state': new_state}
    assert new_state != 'I'
    return old_state


def coherence(file_, lines, words):
    """
    """
    explanations = False
    total = {'R': 0, 'W': 0}
    hits = {'R': 0, 'W': 0}
    index_size = int(math.log(lines, 2))
    caches = [dict() for i in range(4)]

    for line in file_:
        line = line.strip()
        if line == 'v':
            # toggle line-by-line explanation
            explanations = not(explanations)
        elif line == 'p':
            # print out cache contents
            pass
        elif line == 'h':
            # print out hit rate
            pass
        elif line == 'i':
            # print out number of invalidations
            pass
        elif line.startswith('P'):
            instr = make_instruction(line, index_size)
            cache = caches[instr.cpu]
            event = process_instruction(cache, instr)

            # metrics
            total[instr.op] += 1
            if event == 'hit':
                hits[instr.op] += 1

            states = {}
            for idx, cache in enumerate(caches):
                if idx == instr.cpu:
                    states[idx] = local_transition(cache, instr, event)
                elif has_line(cache, instr):
                    states[idx] = remote_transition(cache, instr, event)

            if explanations:
                log(instr, states)
    return total, hits


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
        coherence(file_, args['lines'], args['words'])


if __name__ == '__main__':
    main()
