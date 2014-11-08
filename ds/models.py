"""
Contains models of the components included in the simulation.
"""

from util import Message, send, edge_weight


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

    def __init__(self, orig, dest, orig_id, dest_id):
        self.orig = orig
        self.dest = dest
        self.orig_id = orig_id
        self.dest_id = dest_id

    def __repr__(self):
        return '{}->{}'.format(self.orig, self.dest)

    def __str__(self):
        return '{}->{}'.format(self.orig, self.dest)

    def __eq__(self, other):
        """Edges are undirected."""
        return {self.orig_id, self.dest_id} == {other.orig_id, other.dest_id}

    def __hash__(self):
        """This hash ensures A->B == B->A."""
        return self.orig_id ^ self.dest_id


class Network(object):

    """Simulates the wireless network."""

    def __init__(self, nodes, min_budget):
        """Nodes are only accessible through location."""
        self._nodes = {node.coords: node for node in nodes}
        self.min_budget = min_budget

    def __iter__(self):
        return iter(self._nodes.values())

    def at(self, coords):
        """Return node at specified coordinates."""
        return self._nodes[coords]


class Node(object):

    """Simulates one node in a network."""

    def __init__(self, id_, x, y, energy):
        self.id = id_
        self.leader_id = id_
        self.coords = Coords(x, y)
        self.energy = energy
        self.merged = set()  # nodes that are going to be merged
        self.rejected = set()  # nodes within same component
        self.neighbors = set()  # nodes within radius
        self.edges = set()  # nodes connected to

    def __str__(self):
        return str(self.id)

    def __hash__(self):
        return hash(self.id)

    @property
    def is_leader(self):
        return self.id == self.leader_id

    def receive(self, network, msg_type, src=None, edge=None, leader_id=None, **data):
        """Receive a message from some node."""
        if msg_type == Message.DISCOVER:
            return self.coords
        elif msg_type == Message.NEW_EDGE:
            return self.find_mwoe(network, src=src)
        elif msg_type == Message.ADD_EDGE:
            self.add_edge(network, edge, src=src)
        elif msg_type == Message.CHECK_ID:
            return self.id, self.leader_id
        elif msg_type == Message.ELECTION:
            self.merge(network, leader_id, src=src)
        elif msg_type == Message.ADDED:
            self.merged.add(src)
        else:
            raise Exception('Unknown message type.')

    def forward(self, network, msg_type, src=None, **data):
        """Forward a message to all connected nodes except for source."""
        resps = set()
        src_set = set() if src is None else {src}
        for coords in self.edges - src_set:
            resp = send(network, msg_type, dest=coords, src=self.coords, **data)
            if resp is not None:
                resps.add(resp)
        return resps

    def merge(self, network, leader_id, src=None):
        """Update leader and merge any outstanding edges."""
        # add edges to be merged and reset
        self.edges.update(self.merged)
        self.merged = set()
        # forward the message
        self.forward(network, Message.ELECTION, src=src, leader_id=leader_id)
        # update leader if necessary
        if leader_id > self.leader_id:
            self.leader_id = leader_id

    def add_edge(self, network, edge, src=None):
        """Add edge to connected component."""
        if edge.orig == self.coords:
            # add the edge if it's yours
            self.merged.add(edge.dest)
            # inform the node on the other side
            send(network, Message.ADDED, dest=edge.dest, src=edge.orig)
        else:
            # otherwise forward the message
            self.forward(network, Message.ADD_EDGE, src=src, edge=edge)

    def not_added(self, network):
        """Return nodes not added but not rejected either."""
        edges = set()
        # consider neighbors not yet added or rejected
        for coords in self.neighbors - self.edges - self.rejected:
            node_id, leader_id = send(network, Message.CHECK_ID, src=self.coords, dest=coords)
            if self.leader_id != leader_id:
                # different leader, consider it
                edge = Edge(self.coords, coords, self.id, node_id)
                edges.add(edge)
            else:
                # same leader, never consider again
                self.rejected.add(coords)
        return edges

    def find_mwoe(self, network, src=None):
        """Find minimum weight outgoing edge."""
        edges = self.forward(network, Message.NEW_EDGE, src=src) | self.not_added(network)
        return min(edges, key=edge_weight) if edges else None

    def discover(self, network):
        """Discover nodes within reach."""
        self.neighbors = frozenset(send(network, Message.DISCOVER, src=self.coords))

    def lead(self, network):
        """Informs nodes on edges about shit."""
        min_edge = self.find_mwoe(network)
        if min_edge is not None:
            self.add_edge(network, min_edge)
        return min_edge
