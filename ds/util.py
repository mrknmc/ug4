"""
Contains commonly used utility functions. Also sets up the logging.
"""

import math
import logging

from models import Event, Edge


OUTPUT_FILE = 'log.txt'
DEFAULT_RADIUS = 10

# TODO: uncomment lines here before submission
logging.basicConfig(
    format='%(message)s',
    # filename=OUTPUT_FILE,
    filemode='w',
    level=logging.DEBUG,
    # level=logging.INFO,
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


def send(network, msg_type, dest=None, src=None, **data):
    """Sends a message through wireless on behalf of a node."""
    if dest is None:
        # destination anywhere (discovery)
        reachable = within_radius(network, src)
        return [node.receive(network, msg_type, src=src, **data) for node in reachable]
    else:
        # specific destination
        rcv_node = network.at(dest)
        log('Sending {} from {} to {}'.format(msg_type, src, dest))
        return rcv_node.receive(network, msg_type, src=src, **data)


def energy_cost(edge):
    """Computes the energy cost of sending a message through an edge."""
    return edge_weight(edge) * 1.2


def edge_weight(edge):
    """Computes the edge of a weight."""
    return distance(edge.orig, edge.dest)


def reverse(edge):
    """Reverses an edge. Immutably."""
    return Edge(orig=edge.dest, dest=edge.orig, orig_id=edge.dest_id, dest_id=edge.orig_id)


def distance(coords1, coords2):
    """Euclidean distance between two nodes."""
    dx = coords1.x - coords2.x
    dy = coords1.y - coords2.y
    return math.sqrt(dx * dx + dy * dy)


def log(event, *args):
    """Log events in custom format."""
    if event == Event.BS:
        logging.info('bs {}'.format(','.join(str(node) for node in args)))
    elif event == Event.ADDED:
        for edge in args:
            logging.info('added {}-{}'.format(edge.orig_id, edge.dest_id))
    elif event == Event.ELECTED:
        for node in args:
            logging.info('elected {}'.format(node))
    elif event == Event.BROADCAST:
        edge, energy = args
        logging.info('data from {} to {}, energy:{}'.format(edge.orig_id, edge.dest_id, energy))
    elif event == Event.DEATH:
        logging.info('node down {}'.format(args[0]))
    else:
        logging.debug(event)
