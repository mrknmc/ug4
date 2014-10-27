from enum import Enum
from util import distance


DEFAULT_RADIUS = 10
Message = Enum('Message', ['DISCOVER', 'NEIGHBOR'])


def send(msg_type, node, data=None):
    """Simulates sending a message to a node."""
    return node.receive(msg_type, data=data)


class BaseStation(object):
    """Simulates the all-knowing Base Station."""

    def __init__(self, network):
        self.network = network

    def start_discovery(self):
        """Tell nodes to discover neighbours."""
        for node in self.network.nodes:
            node.discover(self.network)


class Network(object):
    """Simulates the wireless network."""

    def __init__(self, nodes, min_budget):
        """Nodes are only accessible through location."""
        self._nodes = {(node.x, node.y): node for node in nodes}
        self.min_budget = min_budget

    @property
    def nodes(self):
        return self._nodes.values()

    def send(self, msg_type, out_node, in_node=None, data=None):
        """Sends a message on behalf of node."""
        if msg_type == Message.DISCOVER:
            coords = []
            for node in self.nodes:
                if out_node == node:
                    continue  # skip itself
                if distance(out_node, node) <= DEFAULT_RADIUS:
                    coord = send(Message.DISCOVER, node)
                    coords.append(coord)
            return coords

        elif msg_type == Message.NEIGHBOR:
            pass
        else:
            raise Exception('Unknown message type.')


class Node(object):
    """Simulates one node in a network."""

    def __init__(self, id_, x, y, energy):
        self.id = id_
        self.x = x
        self.y = y
        self.energy = energy
        self.neighbors = []

    def __eq__(self, other):
        return self.id == other.id

    def receive(self, msg_type, data=None):
        """Receive a message from some node."""
        if msg_type == Message.DISCOVER:
            # reply with x and y coordinates
            return self.x, self.y
        else:
            pass

    def discover(self, network):
        """Discover nodes within reach."""
        self.neighbors = list(network.send(Message.DISCOVER, self))
