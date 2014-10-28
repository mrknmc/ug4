import logging

from math import sqrt
from enum import Enum
from collections import namedtuple
from util import distance

DEFAULT_RADIUS = 10
OUTPUT_FILE = 'log.txt'

Message = Enum('Message', ['DISCOVER', 'DISCOVER_REPLY', 'NEW_EDGE'])
Component = namedtuple('Component', ['leader', 'nodes'])
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


class Network(object):
    """Simulates the wireless network."""

    def __init__(self, nodes, min_budget):
        """Nodes are only accessible through location."""
        self._nodes = {node.coords: node for node in nodes}
        self.min_budget = min_budget

    @property
    def nodes(self):
        return self._nodes.values()

    def discover(self, out_node):
        """Finds nodes within radius for a node."""
        coords = []
        for rcv_node in self.nodes:
            if out_node == rcv_node:
                continue  # skip itself
            if distance(out_node, rcv_node) <= DEFAULT_RADIUS:
                coord = send(Message.DISCOVER, rcv_node)
                coords.append(coord)
        return coords

    def send(self, msg_type, out_node, orig=None, dest=None, **data):
        """Sends a message through the network on behalf of a node."""
        if msg_type == Message.DISCOVER:
            return self.discover(out_node)
        elif msg_type == Message.NEW_EDGE:
            rcv_node = self._nodes[dest]
            return send(msg_type, rcv_node, **data)
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

    def receive(self, msg_type, orig=None, **data):
        """Receive a message from some node."""
        if msg_type == Message.DISCOVER:
            # reply with x and y coordinates
            return self.coords
        elif msg_type == Message.NEW_EDGE:
            # reply with an edge object
            return self.new_edge(orig)
        else:
            raise Exception('Unknown message type.')

    def new_edge(self, orig=None):
        """"""
        # forward to nodes not received from
        orig = set() if orig is None else {orig}
        forward_nodes = self.edges - orig

        forward_edges = set()
        for coords in forward_nodes:
            edge = self.network.send(Message.NEW_EDGE, self, dest=coords, orig=self.coords)
            forward_edges.add(edge)

        # reply with min coords among neighbors not added
        not_added = (self.neighbors - self.edges)
        not_added = set(Edge(self.coords, coords) for coords in not_added)
        return min(not_added | forward_edges, key=edge_weight)

    def discover(self):
        """Discover nodes within reach."""
        self.neighbors = set(self.network.send(Message.DISCOVER, self, orig=self.coords))

    def lead(self):
        """Informs nodes on edges about shit."""
        edges = []
        for coords in self.edges:
            edge = self.network.send(Message.NEW_EDGE, self, dest=coords, orig=self.coords)
            edges.append(edge)

        edges.append(self.new_edge())

        # find min edge
        print(edges)
        min_edge = min(edges, key=edge_weight)
        # print(min_edge)
        # add min edge to our tree
