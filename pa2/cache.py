import logging

from collections import namedtuple, defaultdict
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
    ('M', 'W', 'hit'): 'M',
    ('S', 'R', 'hit'): 'S',
    ('S', 'W', 'miss'): 'M',
    ('I', 'R', 'miss'): 'S',
    ('I', 'W', 'miss'): 'M',
    (None, 'R', 'miss'): 'S',
    (None, 'W', 'miss'): 'M',
}

MSI_REMOTE_STATES = {
    ('M', 'R', 'miss'): 'S',
    ('M', 'W', 'miss'): 'I',
    ('S', 'R', 'hit'): 'S',  # don't react to R hits
    ('S', 'R', 'miss'): 'S',
    ('S', 'W', 'miss'): 'I',
}

MESI_LOCAL_STATES = {
    ('M', 'R', 'hit'): 'M',
    ('M', 'W', 'hit'): 'M',
    ('E', 'R', 'hit'): 'E',
    ('E', 'W', 'miss'): 'M',
    ('S', 'R', 'hit'): 'S',
    ('S', 'W', 'miss'): 'M',
    ('I', 'W', 'miss'): 'M',
    ('I', 'R', 'miss'): lambda *args: 'E' if exclusive(*args) else 'S',
    (None, 'R', 'miss'): lambda *args: 'E' if exclusive(*args) else 'S',
    (None, 'W', 'miss'): 'M',
}

MESI_REMOTE_STATES = {
    ('M', 'R', 'miss'): 'S',
    ('M', 'W', 'miss'): 'I',
    ('E', 'R', 'miss'): 'S',
    ('E', 'W', 'miss'): 'I',
    ('S', 'R', 'hit'): 'S',  # don't react to R hits
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


def make_line(addr, words, lines):
    """
    Create a cache line.
        :param lines: Number of lines in cache
    """
    index = (addr % lines) // 4
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


def private_access(event, line, mesi):
    """Does the event require shared access."""
    if event.type == 'hit':
        state = get_state(event.cache, line)
        return state in ['M', 'E'] if mesi else state == 'M'


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


def get_tag(cache, line):
    """Retrieve tag associated with index of line"""
    return cache[line.index]['tag']


def get_state(cache, line):
    """Retrieve current state of the line in cache."""
    if line.index in cache and line.tag == get_tag(cache, line):
        return cache[line.index]['state']
    else:
        return None


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


def record_metrics(metrics, line, event, old_state, new_state, remote_states, mesi):
    metrics['total'] += 1
    if event.type == 'hit':
        metrics['hits'] += 1
        if private_access(event, line, mesi):
            metrics['private_access'] += 1
        else:
            metrics['shared_access'] += 1

    # count invalidations
    metrics['invalidations'] += sum(1 for state in remote_states if state == 'I')

    # count when MESI was useful
    if new_state == 'M':
        if old_state == 'E':
            metrics['E->M'] += 1
        elif old_state == 'S':
            metrics['S->M'] += 1

    return metrics


def save_metrics(file_, metrics, metrics_file, mesi):
    """Save metrics to a file."""
    with open(metrics_file, 'a') as f:
        order = ('total', 'hits', 'invalidations', 'shared_access', 'private_access', 'S->M', 'E->M')
        protocol = 'MESI' if mesi else 'MSI'
        hit_rate = metrics['hits'] / float(metrics['total'])
        cols = [file_.name, protocol, hit_rate] + [str(metrics[key]) for key in order]
        csv_line = ','.join(cols) + '\n'
        f.write(csv_line)


def coherence(file_, lines, words, mesi, metrics_file):
    """
    """
    explanations = False
    metrics = defaultdict(int)
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
            print(metrics['hits'] / float(metrics['total']))
        elif line == 'i':
            # print out number of invalidations
            pass
        elif line.startswith('P'):
            inst = make_instruction(line)
            line = make_line(inst.addr, words, lines)
            cache = caches[inst.cpu]
            event = lookup(cache, inst, line)

            if explanations:
                log(inst, line, caches)

            # update local cache
            old_state = get_state(cache, line)
            new_state = transition(cache, inst, line, event, mesi)
            if callable(new_state):
                # new state may depend on args
                new_state = new_state(caches, cache, line)
            set_state(cache, line, event, new_state)

            # update remote caches
            remote_states = []
            for cpu, cache in enumerate(caches):
                if not local(cache, event) and has_line(cache, line):
                    new = transition(cache, inst, line, event, mesi)
                    remote_states.append(new)
                    set_state(cache, line, event, new)

            record_metrics(
                metrics,
                line,
                event,
                old_state,
                new_state,
                remote_states,
                mesi,
            )

        yield caches, metrics

    if metrics_file is not None:
        save_metrics(file_, metrics, metrics_file, mesi)


def main():
    parser = ArgumentParser(description='Run a cache simulator on a given trace file.')
    parser.add_argument('filename', metavar='tracefile', type=str, help='Path to tracefile.')
    parser.add_argument('--lines', type=int, default=1024, help='Number of lines in a cache.')
    parser.add_argument('--words', type=int, default=4, help='Number of words in a line.')
    parser.add_argument('--mesi', dest='mesi', default=False, action='store_true', help='Whether to use MESI protocol.')
    parser.add_argument('--metrics', type=str, default=None, help='Path to metrics file.')
    args = vars(parser.parse_args())
    with open(args['filename']) as file_:
        list(coherence(file_, args['lines'], args['words'], args['mesi'], args['metrics']))


if __name__ == '__main__':
    main()
