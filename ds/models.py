import logging

from math import sqrt
from enum import Enum
from collections import namedtuple
from util import distance

DEFAULT_RADIUS = 10
OUTPUT_FILE = 'log.txt'

Message = Enum('Message', ['DISCOVER', 'NEW_EDGE'])
Component = namedtuple('Component', ['leader', 'nodes'])
logging.basicConfig(
    format='%(message)s',
    filename=OUTPUT_FILE,
    level=logging.INFO
)


def send(msg_type, node, data=None):
    """Simulates sending a message to a node."""
    return node.receive(msg_type, data=data)


class BaseStation(object):
    """Simulates the all-knowing Base Station."""

    def __init__(self, network):
        """Base station has access to the whole network."""
        self.network = network
        self.leaders = [node for node in network.nodes]

    def start_discovery(self):
        """Tell nodes to discover neighbours."""
        for node in self.network.nodes:
            node.discover(self.network)

    def next_level(self):
        """Perform next level of the algorithm."""
        ids = ' '.join(str(leader.id) for leader in self.leaders)
        logging.info('bs {}'.format(ids))
        for leader in self.leaders:
            leader.lead(self.network)


class Network(object):
    """Simulates the wireless network."""

    def __init__(self, nodes, min_budget):
        """Nodes are only accessible through location."""
        self._nodes = {(node.x, node.y): node for node in nodes}
        self.min_budget = min_budget

    @property
    def nodes(self):
        return self._nodes.values()

    def send(self, msg_type, out_node, *coords):
        """Sends a message through the network on behalf of a node."""
        if msg_type == Message.DISCOVER:
            coords = []
            for rcv_node in self.nodes:
                if out_node == rcv_node:
                    continue  # skip itself
                if distance(out_node, rcv_node) <= DEFAULT_RADIUS:
                    coord = send(msg_type, rcv_node)
                    coords.append(coord)
            return coords
        elif msg_type == Message.NEW_EDGE:
            rcv_node = self._nodes[coords]
            return send(msg_type, rcv_node)
        else:
            raise Exception('Unknown message type.')


class Node(object):
    """Simulates one node in a network."""

    def __init__(self, id_, x, y, energy):
        self.id = id_
        self.x = x
        self.y = y
        self.energy = energy
        self.neighbors = set()
        self.edges = set()

    def __eq__(self, other):
        return self.id == other.id

    def distance(self, x, y):
        dx = self.x - x
        dy = self.y - y
        return sqrt(dx * dx + dy * dy)

    def receive(self, msg_type, data=None):
        """Receive a message from some node."""
        if msg_type == Message.DISCOVER:
            # reply with x and y coordinates
            return self.x, self.y
        elif msg_type == Message.NEW_EDGE:
            # reply with min coords among neighbors not added
            # TODO: also, tell all your neighbors to do this, right?
            not_added = self.neighbors - self.edges
            return min(not_added, key=lambda coord: self.distance(*coord))
        else:
            raise Exception('Unknown message type.')

    def discover(self, network):
        """Discover nodes within reach."""
        # network "sends" it on our behalf
        self.neighbors = set(network.send(Message.DISCOVER, self))

    def lead(self, network):
        """Informs nodes on edges about shit."""
        for coords in self.edges:
            network.send(Message.NEW_EDGE, self, coords)
