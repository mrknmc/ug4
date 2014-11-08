"""
Contains commonly used utility functions. Also sets up the logging.
"""

import math
import logging

from enum import Enum

OUTPUT_FILE = 'log.txt'
DEFAULT_RADIUS = 10

Message = Enum('Message', ['DISCOVER', 'ADD_EDGE', 'ADDED', 'NEW_EDGE', 'CHECK_ID', 'ELECTION', 'DEAD'])
Event = Enum('Event', ['ADDED', 'BS', 'ELECTED', 'DEATH'])

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


def kill(node, network):
    """Inform edges that you're dying."""
    for coords in node.edges:
        send(network, Message.DEAD, src=node.coords)
    log(Event.DEAD, node)


def send(network, msg_type, dest=None, **data):
    """Sends a message through wireless on behalf of a node."""
    if dest is None:
        reachable = within_radius(network, data['src'])
        return [node.receive(network, msg_type, **data) for node in reachable]
    else:
        rcv_node = network.at(dest)
        return rcv_node.receive(network, msg_type, **data)


def energy_cost(edge):
    """Computes the energy cost of sending a message through an edge."""
    return edge_weight(distance) * 1.2


def edge_weight(edge):
    """Computes the edge of a weight."""
    return distance(edge.orig, edge.dest)


def distance(coords1, coords2):
    """Euclidean distance between two nodes."""
    dx = coords1.x - coords2.x
    dy = coords1.y - coords2.y
    return math.sqrt(dx * dx + dy * dy)


def log(event, arg):
    """Log events in custom format."""
    if event == Event.BS:
        logging.info('bs {}'.format(','.join(str(node) for node in arg)))
    elif event == Event.ADDED:
        for edge in arg:
            logging.info('added {}-{}'.format(edge.orig_id, edge.dest_id))
    elif event == Event.ELECTED:
        for node in arg:
            logging.info('elected {}'.format(node))
    elif event == Event.DEATH:
        logging.info('node down {}'.format(node))
