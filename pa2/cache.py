import math

from collections import namedtuple
from argparse import ArgumentParser


Event = namedtuple('Event', ['type', 'cache'])
Instruction = namedtuple('Instruction', ['cpu', 'op', 'index', 'tag', 'address'])

ERROR_FORMAT = (
    'P{inst.cpu}: A {type} transition ({old}, {inst.op}, {event.type}) is not valid.'
)

LOG_FORMAT = (
    'A {inst.op} by processor P{inst.cpu} to word {inst.address} looked'
    ' for tag {inst.tag} in cache line {inst.index},'
    ' was found in state {state} in this cache.'
)

LOG_EXTENDED_FORMAT = (
    'A {inst.op} by processor P{inst.cpu} to word {inst.address} looked'
    ' for tag {inst.tag} in cache line {inst.index},'
    ' was found in state {state} in this cache'
    ' and found in states {states} in the caches of {cpus}.'
)

DISALLOWED_LOCAL_TRANSITIONS = (
    ('I', 'R', 'hit'),
    ('I', 'W', 'hit'),
    ('S', 'W', 'hit'),
    ('E', 'W', 'hit'),
)

DISALLOWED_REMOTE_TRANSITIONS = (
    ('I', 'R', 'hit'),
    ('I', 'W', 'hit'),
    ('S', 'W', 'hit'),
    ('E', 'W', 'hit'),
    ('E', 'R', 'hit'),
)

MSI_LOCAL_STATES = {
    ('M', 'R', 'hit'): 'M',
    ('M', 'R', 'miss'): 'S',
    ('M', 'W', 'hit'): 'M',
    ('M', 'W', 'miss'): 'M',
    ('S', 'R', 'hit'): 'S',
    ('S', 'R', 'miss'): 'S',
    ('S', 'W', 'miss'): 'M',
    ('I', 'R', 'miss'): 'S',
    ('I', 'W', 'miss'): 'M',
}

MSI_REMOTE_STATES = {
    ('M', 'R', 'miss'): 'S',
    ('M', 'W', 'miss'): 'I',
    ('S', 'R', 'hit'): 'S',
    ('S', 'R', 'miss'): 'S',
    ('S', 'W', 'miss'): 'I',
}

MESI_LOCAL_STATES = {
    ('M', 'R', 'hit'): 'M',
    ('M', 'R', 'miss'): 'S',  # TODO: verify
    ('M', 'W', 'hit'): 'M',
    ('M', 'W', 'miss'): 'M',  # TODO: verify
    ('E', 'R', 'hit'): 'E',
    ('E', 'R', 'miss'): 'S',  # TODO: verify
    ('E', 'W', 'miss'): 'M',
    ('S', 'R', 'hit'): 'S',
    ('S', 'R', 'miss'): 'S',  # TODO: verify
    ('S', 'W', 'miss'): 'M',  # TODO: inform everyone
    ('I', 'W', 'miss'): 'M',
    ('I', 'R', 'miss'): lambda *args: 'E' if exclusive(*args) else 'S',
}

MESI_REMOTE_STATES = {
    ('M', 'R', 'miss'): 'S',
    ('M', 'W', 'miss'): 'I',
    ('E', 'R', 'miss'): 'S',
    ('E', 'W', 'miss'): 'I',
    ('S', 'R', 'hit'): 'S',  # TODO: verify
    ('S', 'R', 'miss'): 'S',
    ('S', 'W', 'miss'): 'I',
}


def log(inst, states):
    """Log to standard output."""
    out_str = LOG_EXTENDED_FORMAT if len(states) > 1 else LOG_FORMAT
    extra = {
        'inst': inst,
        'state': states[inst.cpu],
        'states': ', '.join(states.values()),
        'cpus': ', '.join('P{}'.format(cpu) for cpu in states),
    }
    print(out_str.format(**extra))


def error(cache, old_state, inst, event):
    extra = {
        'inst': inst,
        'event': event,
        'old': old_state,
        'type': 'local' if local(cache, event) else 'remote',
    }
    return ERROR_FORMAT.format(**extra)


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


def has_line(cache, inst):
    """
    Return true if cache has the line needed by the instruction
        :param cache: Cache we check.
        :param instr: Instruction we check.
        :returns: True if the cache contains the line in valid state.
    """
    return (
        inst.index in cache and
        cache[inst.index]['tag'] == inst.tag and
        cache[inst.index]['state'] != 'I'
    )


def local(cache, event):
    """Is the event local to the cache."""
    return event.cache is cache


def exclusive(caches, l_cache, inst):
    """Does the local cache have exclusive access."""
    return all(cache is l_cache or not has_line(cache, inst) for cache in caches)


def get_state(cache, inst, event):
    """Retrieve current state of the cache."""
    if local(cache, event):
        # TODO: is it ok to assume Invalid if nothing in cache?
        return cache[inst.index]['state'] if inst.index in cache else 'I'
    else:
        return cache[inst.index]['state']


def valid_transition(cache, old_state, inst, event):
    """Check that the transition is valid."""
    if local(cache, event):
        transition = old_state, inst.op, event.type
        return transition not in DISALLOWED_LOCAL_TRANSITIONS
    else:
        transition = old_state, inst.op, event.type
        return all([
            has_line(cache, inst),
            transition not in DISALLOWED_REMOTE_TRANSITIONS,
        ])


def process_instruction(cache, inst):
    """
    Process an instruction.
        :param op: Operation to execute.
        :param instr: Instruction to process.
        :returns: 'hit' or 'miss'.
    """
    # not in cache => miss and replace
    if inst.index not in cache:
        return Event('miss', cache)

    # different tag => miss and replace
    if cache[inst.index]['tag'] != inst.tag:
        return Event('miss', cache)

    # invalid state, write in shared, write in exclusive are misses
    line_state = cache[inst.index]['state']
    if any([
        line_state == 'I',
        line_state == 'S' and inst.op == 'W',
        line_state == 'E' and inst.op == 'W'
    ]):
        return Event('miss', cache)

    # same tag and not invalid state is a hit
    return Event('hit', cache)


def transition(cache, inst, event):
    """
    Transition the cache according to an event.
        :param cache: Cache to transition.
        :param instr: Instruction that was processed.
        :param event: Hit or miss.
        :returns: Tuple of old and new state.
    """
    old_state = get_state(cache, inst, event)
    assert valid_transition(cache, old_state, inst, event), error(cache, old_state, inst, event)

    states = MSI_LOCAL_STATES if local(cache, event) else MSI_REMOTE_STATES
    transition = (old_state, inst.op, event.type)
    new_state = states[transition]
    return old_state, new_state


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
            print(sum(hits.values()) / float(sum(total.values())))
        elif line == 'i':
            # print out number of invalidations
            pass
        elif line.startswith('P'):
            inst = make_instruction(line, index_size)
            cache = caches[inst.cpu]
            event = process_instruction(cache, inst)
            states = {}

            # metrics
            total[inst.op] += 1
            if event.type == 'hit':
                hits[inst.op] += 1

            # update local cache
            old_state, new_state = transition(cache, inst, event)
            states[inst.cpu] = old_state
            # new state may depend on args
            if callable(new_state):
                new_state = new_state(caches, cache, inst)
            cache[inst.index] = {'tag': inst.tag, 'state': new_state}

            # update remote caches
            for idx, cache in enumerate(caches):
                if (not local(cache, event)) and has_line(cache, inst):
                    old_state, new_state = transition(cache, inst, event)
                    states[idx] = old_state
                    cache[inst.index]['state'] = new_state

            if explanations:
                log(inst, states)

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
