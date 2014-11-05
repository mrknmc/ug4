from enum import Enum
from util import log, distance, edge_weight, Event

DEFAULT_RADIUS = 10

Message = Enum('Message', ['DISCOVER', 'ADD_EDGE', 'ADDED', 'NEW_EDGE', 'CHECK_ID', 'ELECTION'])


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


class Network(object):

    """Simulates the wireless network."""

    def __init__(self, nodes, min_budget):
        """Nodes are only accessible through location."""
        self._nodes = {node.coords: node for node in nodes}
        self.min_budget = min_budget

    @property
    def nodes(self):
        return self._nodes.values()

    def within_radius(self, src_coords, radius=DEFAULT_RADIUS):
        """Return nodes within radius of the coordinates."""
        for node in self.nodes:
            # exclude the sender
            dest_coords = node.coords
            if dest_coords == src_coords:
                continue
            elif distance(dest_coords, src_coords) < radius:
                yield node

    def send(self, msg_type, dest=None, **data):
        """Sends a message through wireless on behalf of a node."""
        if dest is None:
            reachable = self.within_radius(data['src'])
            return [node.receive(msg_type, **data) for node in reachable]
        else:
            rcv_node = self._nodes[dest]
            return rcv_node.receive(msg_type, **data)


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
        """Update leader and merge any outstanding edges."""
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
        """Add an edge."""
        # add the edge if it's yours
        if edge.orig == self.coords:
            self.merged.add(edge.dest)
            # inform the node on the other side
            self.network.send(Message.ADDED, dest=edge.dest, src=edge.orig)
            log(Event.ADDED, self.id, edge.dest_id)
            # log('added', self.id, edge.dest_id)
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

    def discover(self, network):
        """Discover nodes within reach."""
        self.neighbors = set(network.send(Message.DISCOVER, src=self.coords))

    def lead(self):
        """Informs nodes on edges about shit."""
        min_edge = self.new_edge()
        if min_edge is not None:
            self.add_edge(min_edge)
        return min_edge

    def merge(self):
        """Merge components."""
        self.update_leader(self.id)
