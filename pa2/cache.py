from collections import namedtuple
from argparse import ArgumentParser


Event = namedtuple('Event', ['type', 'cache'])
Line = namedtuple('Line', ['index', 'tag'])
Instruction = namedtuple('Instruction', ['cpu', 'op', 'addr'])

LOG_FORMAT = (
    'A {inst.op} by processor P{inst.cpu} to word {inst.addr} looked for tag'
    ' {line.tag} in cache line {line.index},'
    ' was found in state {state} in this cache.'
)

LOG_EXTENDED_FORMAT = (
    'A {inst.op} by processor P{inst.cpu} to word {inst.addr} looked for tag'
    ' {line.tag} in cache line {line.index}, was found in state {state}'
    ' in this cache and found in states {states} in the caches of {cpus}.'
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


def log(inst, line, event, caches):
    """Log to stdout."""
    local_state = get_state(caches[inst.cpu], line, event)
    # get states of line from caches that have it
    caches = [(cpu, c) for (cpu, c) in enumerate(caches) if has_line(c, line)]
    states = [(cpu, get_state(c, line, event)) for (cpu, c) in caches]
    out_str = LOG_EXTENDED_FORMAT if len(states) > 1 else LOG_FORMAT
    extra = {
        'inst': inst,
        'line': line,
        'state': local_state,
        'states': ', '.join(state for (cpu, state) in states),
        'cpus': ', '.join('P{}'.format(cpu) for (cpu, state) in states),
    }
    print(out_str.format(**extra))


def make_line(addr, lines):
    """
    Create a cache line.
        :param lines: Number of lines in cache
    """
    index = addr % lines
    tag = addr / lines
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
        cache[line.index] = {'tag': line.tag, 'state': new_state}
    else:
        cache[line.index]['state'] = new_state


def get_state(cache, line, event):
    """Retrieve current state of the line in cache."""
    if local(cache, event):
        # TODO: is it ok to assume Invalid if nothing in cache?
        return cache[line.index]['state'] if line.index in cache else 'I'
    else:
        return cache[line.index]['state']


def make_event(cache, inst, line):
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


def transition(cache, inst, line, event):
    """
    Transition the cache according to an event.
        :param cache: Cache to transition.
        :param instr: Instruction that was processed.
        :param event: Hit or miss.
        :returns: Tuple of old and new state.
    """
    old_state = get_state(cache, line, event)
    states = MSI_LOCAL_STATES if local(cache, event) else MSI_REMOTE_STATES
    transition = (old_state, inst.op, event.type)
    return states[transition]


def coherence(file_, lines, words):
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
            event = make_event(cache, inst, line)

            # metrics
            total[inst.op] += 1
            if event.type == 'hit':
                hits[inst.op] += 1

            # logging
            if explanations:
                log(inst, line, event, caches)

            # update local & remote caches
            for cpu, cache in enumerate(caches):
                if local(cache, event) or has_line(cache, line):
                    # make a transition
                    new_state = transition(cache, inst, line, event)
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
    args = vars(parser.parse_args())
    with open(args['filename']) as file_:
        list(coherence(file_, args['lines'], args['words']))


if __name__ == '__main__':
    main()
