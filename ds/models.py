import logging

from math import sqrt
from enum import Enum
from util import distance

DEFAULT_RADIUS = 10
OUTPUT_FILE = 'log.txt'

Message = Enum('Message', ['DISCOVER', 'ADD_EDGE', 'ADDED', 'NEW_EDGE', 'CHECK_ID', 'ELECTION'])


logging.basicConfig(
    format='%(message)s',
    filename=OUTPUT_FILE,
    filemode='w',
    # level=logging.DEBUG,
    level=logging.INFO,
)


class Coords(object):

    """Represents location of a Node."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return '[{},{}]'.format(self.x, self.y)

    def __str__(self):
        return '[{},{}]'.format(self.x, self.y)


class Edge(object):

    """Represents an edge from some coordinates to some other coordinates."""

    def __init__(self, orig, dest, dest_id):
        self.orig = orig
        self.dest = dest
        self.dest_id = dest_id

    def __repr__(self):
        return '{}->{}'.format(self.orig, self.dest)

    def __str__(self):
        return '{}->{}'.format(self.orig, self.dest)


def log(event, *args):
    """Log event to output."""
    out_args = ' '.join(str(arg) for arg in args)
    logging.info('{} {}'.format(event, out_args))


def edge_weight(edge):
    """Computes the edge of a weight."""
    dx = edge.orig.x - edge.dest.x
    dy = edge.orig.y - edge.dest.y
    return sqrt(dx * dx + dy * dy)


def send(msg_type, node, **data):
    """Simulates sending a message to a node."""
    return node.receive(msg_type, **data)


class BaseStation(object):
    """Simulates the all-knowing Base Station."""

    def __init__(self, network):
        """Base station has access to the whole network."""
        self.network = network

    def start_discovery(self):
        """Tell nodes to discover neighbours."""
        for node in self.network.nodes:
            node.discover()

    def next_level(self):
        """Perform next level of the algorithm."""
        leaders = set(self.network.nodes)
        while len(leaders) > 1:
            log('bs', *leaders)
            any([leader.lead() for leader in leaders])
            for leader in leaders:
                leader.merge()
            # new leaders are going to be a subset of previous leaders
            leaders = set(lead for lead in leaders if lead.leader_id == lead.id)


class Network(object):

    """Simulates the wireless network."""

    def __init__(self, nodes, min_budget):
        """Nodes are only accessible through location."""
        self._nodes = {node.coords: node for node in nodes}
        self._id_map = {node.id: node for node in nodes}
        self.min_budget = min_budget

    def get_node(self, id_):
        return self._id_map[id_]

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
        # logging.debug(
        #     'Sending {} from {} to {}.'.format(
        #         msg_type.name,
        #         src,
        #         '' if dest is None else dest
        #     )
        # )
        if msg_type == Message.DISCOVER:
            return self.discover(src)
        elif msg_type == Message.ADDED:
            rcv_node = self._nodes[dest]
            send(msg_type, rcv_node, src=src, **data)
        else:
            rcv_node = self._nodes[dest]
            return send(msg_type, rcv_node, src=src, **data)


class Node(object):
    """Simulates one node in a network."""

    def __init__(self, id_, x, y, energy):
        self.id = id_
        self.leader_id = id_
        self.coords = Coords(x, y)
        self.energy = energy
        self.merged = set()  # nodes that are merged
        self.rejected = set()  # nodes within same component
        self.neighbors = set()  # nodes within radius
        self.edges = set()  # nodes connected to

    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        return str(self.id)

    def __hash__(self):
        return hash(self.id)

    def receive(self, msg_type, src=None, edge=None, leader_id=None, **data):
        """Receive a message from some node."""
        if msg_type == Message.DISCOVER:
            return self.coords
        elif msg_type == Message.NEW_EDGE:
            return self.new_edge(src=src)
        elif msg_type == Message.ADD_EDGE:
            self.add_edge(edge, src=src)
        elif msg_type == Message.CHECK_ID:
            return self.id, self.leader_id
        elif msg_type == Message.ELECTION:
            self.update_leader(leader_id, src=src)
        elif msg_type == Message.ADDED:
            # spec says inform leader but why?
            # to update other nodes with merged edge?
            self.merged.add(src)
        else:
            raise Exception('Unknown message type.')

    def forward(self, msg_type, src=None, **data):
        """Forward a message to all connected nodes except for source."""
        resps = set()
        src_set = set() if src is None else {src}
        # log('FORWARDING TO {}'.format(self.edges - src_set))
        for coords in self.edges - src_set:
            resp = self.network.send(msg_type, dest=coords, src=self.coords, **data)
            resps.add(resp)
        return resps

    def update_leader(self, leader_id, src=None):
        """"""
        # add edges to be merged and reset
        # log('MERGING {} AND {}'.format(self.coords, self.merged))
        self.edges.update(self.merged)
        self.merged = set()
        # forward the message
        self.forward(Message.ELECTION, src=src, leader_id=leader_id)
        # update leader if necessary
        if leader_id > self.leader_id:
            self.leader_id = leader_id

    def add_edge(self, edge, src=None):
        """"""
        # add the edge if it's yours
        if edge.orig == self.coords:
            self.merged.add(edge.dest)
            # inform the node on the other side
            self.network.send(Message.ADDED, dest=edge.dest, src=edge.orig)
            log('added', self.id, edge.dest_id)
        # otherwise forward the message
        else:
            self.forward(Message.ADD_EDGE, src=src, edge=edge)

    def not_added(self):
        """Return nodes not added but not rejected either."""
        edges = set()
        # consider neighbors not yet added or rejected
        for coords in self.neighbors - self.edges - self.rejected:
            node_id, leader_id = self.network.send(Message.CHECK_ID, src=self.coords, dest=coords)
            if self.leader_id != leader_id:
                # different leader, consider it
                edge = Edge(self.coords, coords, node_id)
                edges.add(edge)
            else:
                # same leader, never consider again
                self.rejected.add(coords)
        # log('Nodes connectible to {} are {}'.format(self.id, edges))
        return edges

    def new_edge(self, src=None):
        """"""
        nodes = self.forward(Message.NEW_EDGE, src=src) | self.not_added()
        if nodes:
            return min(nodes, key=edge_weight)
        else:
            return None

    def discover(self):
        """Discover nodes within reach."""
        self.neighbors = set(self.network.send(Message.DISCOVER, src=self.coords))

    def lead(self):
        """Informs nodes on edges about shit."""
        min_edge = self.new_edge()
        if min_edge is not None:
            self.add_edge(min_edge)
        return min_edge

    def merge(self):
        """"""
        self.update_leader(self.id)
