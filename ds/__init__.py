"""
1. The base­station alerts all the nodes to start constructing the MST
2. Each node discovers the other nodes in its proximity
3. The leader of a connected component broadcasts a message inside the component for
each node to identify a new edge to add to the MST
4. Each node chooses the link with the lowest weight to add, and sends it to the leader of its
component in a convergecast
5. The leader of a component chooses which link to add and broadcasts (floods in the tree)
its decision.
6. Once all the leaders have made their decisions, the beacon broadcasts a “merge”
message. All the leaders now flood (in the tree) their id, and in each connected component,
    the leader with the highest id becomes the leader of the entire component for the next level.
7. The base­station waits for all the components to finish before moving to the next level and
    broadcasts a beacon to start next level
8. The next level starts again from step 3.
9. The algorithm finishes when there is no mode link added to the MST in a level.
"""

import math


INPUT_FILE = 'input.txt'
OUTPUT_FILE = 'log.txt'
RADIUS = 10

DISCOVER = 'discover'
NEIGHBOR = 'neighbor'


class BaseStation(object):
    """Simulates the all-knowing Base Station."""

    def __init__(self, network):
        self.network = network

    def start_discovery(self):
        for node in self.network:
            node.discover()


class Network(object):
    """Simulates the wireless network."""

    def __init__(self, nodes):
        self.nodes = nodes

    def discover(self, out_node):
        """Sends a discover message to a node if within radius."""
        for node in self.nodes:
            if out_node == node:
                continue  # skip myself
            weight = distance(out_node, node)
            if weight <= RADIUS:
                # send a discover message
                x, y = send(DISCOVER, node)


class Node(object):
    """Simulates one node in a network."""

    def __init__(self, id_, x, y, energy):
        self.id = id_
        self.x = x
        self.y = y
        self.energy = energy
        self.neighbs = []

    def __eq__(self, other):
        return self.id == other.id

    def receive(self, type, node, data=None):
        """Receive a message from some node."""
        if type == DISCOVER:
            # reply with x and y coordinates
            return self.x, self.y
        else:
            pass

    def discover(self, network):
        """Discover nodes within reach."""
        for node in network.discover(self):
            self.neighbs.append(node)


def distance(node1, node2):
    """Euclidean distance between two nodes."""
    dx = node1.x - node2.x
    dy = node1.y - node2.y
    return math.sqrt(dx * dx + dy * dy)


def send(type_, node, data=None):
    """Simulates sending a message to a node."""
    node.receive(type_, data=data)


def parse_file(path):
    """Parse the input file."""
    with open(path) as input_file:
        min_budget = float(input_file.next())
        bcsts = []
        nodes = {}
        for line in input_file:
            if line.startswith('node'):
                node_id, x, y, energy = line.split(', ')
                node_id = int(node_id.lstrip('node '))
                node = Node(node_id, x, y, energy)
                nodes.append(node)
            else:
                bcst = line.lstrip('bcst from ')
                bcsts.append(bcst)
    return min_budget, nodes, bcsts


def main():
    """"""
    min_budget, nodes, bcsts = parse_file(INPUT_FILE)
    network = Network(nodes)
    bs = BaseStation(network)

    bs.start_discovery()


if __name__ == '__main__':
    main()
