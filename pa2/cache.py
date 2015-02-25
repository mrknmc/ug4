import logging

from collections import namedtuple
from argparse import ArgumentParser


Event = namedtuple('Event', ['type', 'cache'])
Line = namedtuple('Line', ['index', 'tag'])
Instruction = namedtuple('Instruction', ['cpu', 'op', 'addr'])

FORMAT = 'P%(cpu)s - %(op)s - %(addr)-0.5d: %(msg)s'
NOT_FOUND = 'Tag {tag:02} not found in line {index:04} of local cache.'
FOUND = 'Tag {tag:02} found in state {state} in line {index:04} of local cache.'
FOUND_MORE = ' Found in following remote caches {}.'

logging.basicConfig(format=FORMAT, level=logging.INFO)

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
    (None, 'R', 'miss'): 'S',  # TODO: verify
    (None, 'W', 'miss'): 'M',  # TODO: verify
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
    (None, 'R', 'miss'): lambda *args: 'E' if exclusive(*args) else 'S',  # TODO: verify
    (None, 'W', 'miss'): 'M',  # TODO: verify
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


def log(inst, line, caches):
    """Log to stdout."""
    local_state = get_state(caches[inst.cpu], line)
    out_str = NOT_FOUND if local_state is None else FOUND
    out_str = out_str.format(tag=line.tag, index=line.index, state=local_state)
    # get states of line from caches that have it
    remote_states = []
    for cpu, cache in enumerate(caches):
        if has_line(cache, line) and cpu != inst.cpu:
            remote_states.append((cpu, get_state(cache, line)))
    if remote_states:
        cpu_str = ', '.join('P{}: {}'.format(*state) for state in remote_states)
        out_str += FOUND_MORE.format(cpu_str)
    extra = {'op': inst.op, 'cpu': inst.cpu, 'addr': inst.addr}
    logging.info(out_str, extra=extra)


def make_line(addr, lines):
    """
    Create a cache line.
        :param lines: Number of lines in cache
    """
    index = addr % lines
    tag = addr // lines
    return Line(index, tag)


def make_instruction(line):
    """
    Create an instruction.
        :param line: Line to parse.
        :returns: CPU id, operator, and addr.
    """
    cpu, op, addr = line.split()
    addr = int(addr)
    cpu = int(cpu.lstrip('P'))  # strip P from CPU number
    return Instruction(cpu, op, addr)


def has_line(cache, line):
    """
    Return true if cache has the line needed by the instruction
        :param cache: Cache we check.
        :param instr: Instruction we check.
        :returns: True if the cache contains the line in valid state.
    """
    return (
        line.index in cache and
        cache[line.index]['tag'] == line.tag and
        cache[line.index]['state'] != 'I'
    )


def local(cache, event):
    """Is the event local to the cache."""
    return event.cache is cache


def exclusive(caches, l_cache, line):
    """Does the local cache have exclusive access."""
    return all(cache is l_cache or not has_line(cache, line) for cache in caches)


def set_state(cache, line, event, new_state):
    """Set state of the line in cache."""
    if local(cache, event):
        # could be eviction => replace tag as well
        cache[line.index] = {'tag': line.tag, 'state': new_state}
    else:
        cache[line.index]['state'] = new_state


def get_state(cache, line):
    """Retrieve current state of the line in cache."""
    return cache.get(line.index, {}).get('state', None)


def lookup(cache, inst, line):
    """
    Process an instruction.
        :param op: Operation to execute.
        :param instr: Instruction to process.
        :returns: 'hit' or 'miss'.
    """
    # not in cache => miss and replace
    if line.index not in cache:
        return Event('miss', cache)

    # different tag => miss and replace
    if cache[line.index]['tag'] != line.tag:
        return Event('miss', cache)

    # invalid state, write in shared or exclusive are misses
    state = cache[line.index]['state']
    if state == 'I' or (state in ['S', 'E'] and inst.op == 'W'):
        return Event('miss', cache)

    # same tag and not invalid state is a hit
    return Event('hit', cache)


def transition(cache, inst, line, event, mesi):
    """
    Transition the cache according to an event.
        :param cache: Cache to transition.
        :param instr: Instruction that was processed.
        :param event: Hit or miss.
        :returns: Tuple of old and new state.
    """
    old_state = get_state(cache, line)
    if mesi:
        states = MESI_LOCAL_STATES if local(cache, event) else MESI_REMOTE_STATES
    else:
        states = MSI_LOCAL_STATES if local(cache, event) else MSI_REMOTE_STATES
    transition = (old_state, inst.op, event.type)
    return states[transition]


def coherence(file_, lines, words, mesi):
    """
    """
    explanations = False
    total = {'R': 0, 'W': 0}
    hits = {'R': 0, 'W': 0}
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
            inst = make_instruction(line)
            line = make_line(inst.addr, lines)
            cache = caches[inst.cpu]
            event = lookup(cache, inst, line)

            # metrics
            total[inst.op] += 1
            if event.type == 'hit':
                hits[inst.op] += 1

            # logging
            if explanations:
                log(inst, line, caches)

            # update local & remote caches
            for cpu, cache in enumerate(caches):
                if local(cache, event) or has_line(cache, line):
                    # make a transition
                    new_state = transition(cache, inst, line, event, mesi)
                    # new state may depend on args
                    if callable(new_state):
                        new_state = new_state(caches, cache, line)
                    # set new state
                    set_state(cache, line, event, new_state)

        yield caches


def main():
    parser = ArgumentParser(description='Run a cache simulator on a given trace file.')
    parser.add_argument('filename', metavar='tracefile', type=str, help='Path to tracefile.')
    parser.add_argument('--lines', type=int, default=1024, help='Number of lines in a cache.')
    parser.add_argument('--words', type=int, default=4, help='Number of words in a line.')
    parser.add_argument('--mesi', dest='mesi', default=False, action='store_true', help='Whether to use MESI states.')
    args = vars(parser.parse_args())
    with open(args['filename']) as file_:
        list(coherence(file_, args['lines'], args['words'], args['mesi']))


if __name__ == '__main__':
    main()
