import logging

from math import sqrt
from enum import Enum
from collections import namedtuple
from util import distance

DEFAULT_RADIUS = 10
OUTPUT_FILE = 'log.txt'

Message = Enum('Message', ['DISCOVER', 'ADD_EDGE', 'NEW_EDGE'])
Edge = namedtuple('Edge', ['orig', 'dest'])
Coords = namedtuple('Coords', ['x', 'y'])

logging.basicConfig(
    format='%(message)s',
    filename=OUTPUT_FILE,
    filemode='w',
    level=logging.INFO,
)


def edge_weight(edge):
    dx = edge.orig.x - edge.orig.x
    dy = edge.dest.y - edge.dest.y
    return sqrt(dx * dx + dy * dy)


def send(msg_type, node, **data):
    """Simulates sending a message to a node."""
    return node.receive(msg_type, **data)


class BaseStation(object):
    """Simulates the all-knowing Base Station."""

    def __init__(self, network):
        """Base station has access to the whole network."""
        self.network = network
        self.leaders = [node for node in network.nodes]

    def start_discovery(self):
        """Tell nodes to discover neighbours."""
        for node in self.network.nodes:
            node.discover()

    def next_level(self):
        """Perform next level of the algorithm."""
        ids = ' '.join(str(leader) for leader in self.leaders)
        logging.info('bs {}'.format(ids))
        for leader in self.leaders:
            leader.lead()
        for leader in self.leaders:
            leader.merge()


class Network(object):
    """Simulates the wireless network."""

    def __init__(self, nodes, min_budget):
        """Nodes are only accessible through location."""
        self._nodes = {node.coords: node for node in nodes}
        self.min_budget = min_budget

    @property
    def nodes(self):
        return self._nodes.values()

    def discover(self, src):
        """Finds nodes within radius for a node."""
        for coords, rcv_node in self._nodes.items():
            if src == coords:
                continue  # skip yourself
            if distance(src, coords) <= DEFAULT_RADIUS:
                yield send(Message.DISCOVER, rcv_node)

    def send(self, msg_type, dest=None, src=None, **data):
        """Sends a message through the network on behalf of a node."""
        if msg_type == Message.DISCOVER:
            return self.discover(src)
        elif msg_type == Message.NEW_EDGE or msg_type == Message.ADD_EDGE:
            rcv_node = self._nodes[dest]
            return send(msg_type, rcv_node, src=src, **data)
        else:
            raise Exception('Unknown message type.')


class Node(object):
    """Simulates one node in a network."""

    def __init__(self, id_, x, y, energy):
        self.id = id_
        self.coords = Coords(x, y)
        self.energy = energy
        self.neighbors = set()  # nodes within radius
        self.edges = set()  # nodes connected to

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return str(self.id)

    def receive(self, msg_type, src=None, edge=None, **data):
        """Receive a message from some node."""
        if msg_type == Message.DISCOVER:
            return self.coords
        elif msg_type == Message.NEW_EDGE:
            return self.new_edge(src=src)
        elif msg_type == Message.ADD_EDGE:
            return self.add_edge(edge, src=src)
        else:
            raise Exception('Unknown message type.')

    def forward(self, msg_type, src=None, **data):
        """Forward a message to all connected nodes except for origin."""
        src_set = set() if src is None else {src}
        for coords in self.edges - src_set:
            yield self.network.send(msg_type, dest=coords, orig=self.coords, **data)

    def add_edge(self, edge, src=None):
        """"""
        # add the edge if it's yours
        if edge.orig == self.coords:
            self.edges.add(edge.dest)
            logging.info('added {}­ {}'.format(self.id, edge.dest))
        # otherwise forward the message
        else:
            self.forward(Message.ADD_EDGE, src=src, edge=edge)

    @property
    def not_added(self):
        return self.neighbors - self.edges

    def new_edge(self, src=None):
        """"""
        # forward the message
        forward_edges = set(self.forward(Message.NEW_EDGE, src=src))
        # reply with min coords among neighbors not added
        not_added = set(Edge(self.coords, coords) for coords in self.not_added)
        return min(not_added | forward_edges, key=edge_weight)

    def discover(self):
        """Discover nodes within reach."""
        self.neighbors = set(self.network.send(Message.DISCOVER, src=self.coords))

    def lead(self):
        """Informs nodes on edges about shit."""
        min_edge = self.new_edge()
        self.add_edge(min_edge)

    def merge(self):
        """"""
        pass
