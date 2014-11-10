"""
"""

from util import send, edge_weight, energy_cost, reverse, log
from models import Coords, Message, Edge, Event


class Node(object):

    """Simulates one node in a network."""

    def __init__(self, id_, x, y, energy):
        self.id = id_
        self.leader_id = id_
        self.coords = Coords(x, y)
        self.energy = energy
        self.merged = set()  # nodes that are going to be merged
        self.dead = set()  # nodes that died
        self.rejected = set()  # nodes within same component added by others
        self.neighbors = set()  # nodes within radius
        self.edges = set()  # edges to neighbor nodes

    def __str__(self):
        return str(self.id)

    def __hash__(self):
        return hash(self.id)

    @property
    def is_leader(self):
        """Check whether this node is a leader."""
        return self.id == self.leader_id

    @property
    def edge_coords(self):
        """Return coordinates of nodes there is an edge to."""
        return set(edge.dest for edge in self.edges)

    def broadcast_cost(self, src):
        """Return cost associated with sending readings to all children."""
        return sum(energy_cost(edge) for edge in self.edges if edge.dest != src)

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
            self.merged.add(reverse(edge))
        elif msg_type == Message.DEAD:
            # TODO: find a replacement node
            self.dead.add(reverse(edge))
        elif msg_type == Message.BROADCAST:
            self.broadcast(network, src=src)
        else:
            raise Exception('Unknown message type.')

    def forward(self, network, msg_type, src=None, **data):
        """Forward a message to all connected nodes except for source."""
        resps = set()
        src_set = set() if src is None else {src}
        for coords in self.edge_coords - src_set:
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
            self.merged.add(edge)
            # inform the node on the other side
            send(network, Message.ADDED, dest=edge.dest, edge=edge)
        else:
            # otherwise forward the message
            self.forward(network, Message.ADD_EDGE, src=src, edge=edge)

    def not_added(self, network):
        """Return nodes not added but not rejected either."""
        edges = set()
        # consider neighbors not yet added or rejected
        for coords in self.neighbors - self.rejected - self.edge_coords:
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
        """Lead a round of the MST algorithm."""
        min_edge = self.find_mwoe(network)
        if min_edge is not None:
            self.add_edge(network, min_edge)
        return min_edge

    def die(self, network):
        """Inform edges that you're dying."""
        for edge in self.edges:
            send(network, Message.DEAD, src=edge.orig, dest=edge.dest, edge=edge)
        log(Event.DEATH, self.id)

    def broadcast(self, network, src=None):
        """Broadcast some sensor readings to the whole network."""
        dead_edges = set()
        for edge in self.edges:
            if edge.dest == src or edge in self.dead:
                continue  # don't send to source or dead nodes
            cost = energy_cost(edge)
            if cost < self.energy:
                # we have energy to send it
                self.energy -= cost
                log(Event.BROADCAST, edge, self.energy)
                send(network, Message.BROADCAST, dest=edge.dest, src=self.coords, edge=edge)
                # check if dead
                if self.energy < network.min_budget:
                    self.die(network)
                    break
            else:
                # no energy to send it
                dead_edges.add(edge)

        # dead edges cannot be used anymore their cost is higher than energy
        self.edges.difference_update(dead_edges)
