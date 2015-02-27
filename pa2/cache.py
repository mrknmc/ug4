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
    Translate an address into a Line.
        :param addr: Address to translate.
        :param words: Number of words in a line.
        :param lines: Number of lines in a cache.
    """
    index = (addr % lines) // words
    tag = addr // (words * lines)
    return Line(index, tag)


def make_instruction(line):
    """
    Parse a line of file into an Instruction.
        :param line: Line of file to parse.
    """
    cpu, op, addr = line.split()
    addr = int(addr)
    cpu = int(cpu.lstrip('P'))  # strip P from CPU number
    return Instruction(cpu, op, addr)


def has_line(cache, line):
    """
    Return true if cache has the line.
        :param cache: Cache we check.
        :param line: Line we check.
    """
    return (
        line.index in cache and
        cache[line.index]['tag'] == line.tag and
        cache[line.index]['state'] != 'I'
    )


def private_access(event, line, mesi):
    """
    Is the event performed on a cache in private state.
        :param event: Event that occurred.
        :param line: Line we check.
        :param mesi: Are we using MESI protocol.
    """
    if event.type == 'hit':
        state = get_state(event.cache, line)
        return state in ['M', 'E'] if mesi else state == 'M'


def local(cache, event):
    """Is the event local to the cache."""
    return event.cache is cache


def exclusive(caches, l_cache, line):
    """Does the local cache have exclusive access.
        :param caches: All the caches of the system.
        :param l_cache: Cache we are checking for exclusive access.
        :param line: Line we are checking for exclusive access.
    """
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
    Lookup a line in cache.
        :param cache: Cache used for lookup.
        :param inst: Instruction to process.
        :param Line: Line used for lookup.
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
    Transition the line in cache according to an event.
        :param cache: Cache to transition.
        :param inst: Instruction that was processed.
        :param line: Line we are transitioning.
        :param event: Event that occured.
        :param mesi: Are we using MESI protocol.
    """
    old_state = get_state(cache, line)
    if mesi:
        states = MESI_LOCAL_STATES if local(cache, event) else MESI_REMOTE_STATES
    else:
        states = MSI_LOCAL_STATES if local(cache, event) else MSI_REMOTE_STATES
    transition = (old_state, inst.op, event.type)
    return states[transition]


def record_metrics(metrics, line, event, old_state, new_state, remote_states, mesi):
    """
    Record what happened in current iteration into the metrics.
        :param metrics: The metrics dictionary.
        :param line: The cache line involved.
        :param event: The event that occured.
        :param old_state: The previous state of local cache.
        :param new_state: The new state of local cache.
        :param remote_states: The new states of remote caches.
        :param mesi: Are we using MESI protocol.
    """
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


def save_metrics(file_, metrics, metrics_file, mesi, lines, words):
    """Save metrics to a file."""
    with open(metrics_file, 'a') as f:
        order = ('total', 'hits', 'invalidations', 'shared_access', 'private_access', 'S->M', 'E->M')
        protocol = 'MESI' if mesi else 'MSI'
        hit_rate = str(metrics['hits'] / float(metrics['total']))
        cols = [file_.name, protocol, hit_rate, str(lines), str(words)] + [str(metrics[key]) for key in order]
        csv_line = ','.join(cols) + '\n'
        f.write(csv_line)


def coherence(file_, lines, words, mesi, metrics_file):
    """
    Generator that processes the file and executes the algorithm.
        :param file_: File to process.
        :param lines: Number of lines in a cache.
        :param words: Number of words in a line.
        :param mesi: Are we using MESI protocol.
        :param metrics_file: File to save metrics to.
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
        save_metrics(file_, metrics, metrics_file, mesi, lines, words)


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
