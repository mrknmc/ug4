import math
import logging

from enum import Enum

OUTPUT_FILE = 'log.txt'
DEFAULT_RADIUS = 10

Event = Enum('Event', ['ADDED', 'BS', 'ELECTED'])

logging.basicConfig(
    format='%(message)s',
    filename=OUTPUT_FILE,
    filemode='w',
    # level=logging.DEBUG,
    level=logging.INFO,
)


def within_radius(network, src_coords, radius=DEFAULT_RADIUS):
    """Return nodes within radius of the coordinates."""
    for node in network:
        # exclude the sender
        dest_coords = node.coords
        if dest_coords == src_coords:
            continue
        elif distance(dest_coords, src_coords) < radius:
            yield node


def send(network, msg_type, dest=None, **data):
    """Sends a message through wireless on behalf of a node."""
    if dest is None:
        reachable = within_radius(network, data['src'])
        return [node.receive(network, msg_type, **data) for node in reachable]
    else:
        rcv_node = network.at(dest)
        return rcv_node.receive(network, msg_type, **data)


def edge_weight(edge):
    """Computes the edge of a weight."""
    return distance(edge.orig, edge.dest)


def distance(coords1, coords2):
    """Euclidean distance between two nodes."""
    dx = coords1.x - coords2.x
    dy = coords1.y - coords2.y
    return math.sqrt(dx * dx + dy * dy)


def log(event, *args):
    """Log events in custom format."""
    if event == Event.BS:
        logging.info('bs {}'.format(','.join(map(str, args))))
    elif event == Event.ADDED:
        orig, dest = args
        logging.info('added {}-{}'.format(orig, dest))
    elif event == Event.ELECTED:
        logging.info('elected {}'.format(*args))
    else:
        out_args = ' '.join(str(arg) for arg in args)
        logging.info('{} {}'.format(event, out_args))
