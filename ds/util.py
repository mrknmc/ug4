import math
import logging

from enum import Enum

OUTPUT_FILE = 'log.txt'

Event = Enum('Event', ['ADDED', 'BS', 'ELECTED'])

logging.basicConfig(
    format='%(message)s',
    filename=OUTPUT_FILE,
    filemode='w',
    # level=logging.DEBUG,
    level=logging.INFO,
)


def edge_weight(edge):
    """Computes the edge of a weight."""
    return distance(edge.orig, edge.dest)


def send(msg_type, node, **data):
    """Simulates sending a message to a node."""
    return node.receive(msg_type, **data)


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
        logging.info('added {}-{}'.format(args[0], args[1]))
    elif event == Event.ELECTED:
        logging.info('elected {}'.format(args[0]))
    else:
        out_args = ' '.join(str(arg) for arg in args)
        logging.info('{} {}'.format(event, out_args))
