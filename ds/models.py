"""
Contains models of the components included in the simulation.
"""

from enum import Enum, unique


@unique
class Event(Enum):

    """Represents event type."""

    ADDED = 0
    BS = 1
    ELECTED = 2
    DEATH = 3


@unique
class Message(Enum):

    """Represents message type."""

    DISCOVER = 0
    ADD_EDGE = 1
    ADDED = 2
    NEW_EDGE = 3
    CHECK_ID = 4
    ELECTION = 5
    DEAD = 6


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
        self._id_map = {node.id: node for node in nodes}
        self.min_budget = min_budget

    def __iter__(self):
        return iter(self._nodes.values())

    def get(self, id_):
        """Return node with specified it."""
        return self._id_map[id_]

    def at(self, coords):
        """Return node at specified coordinates."""
        return self._nodes[coords]
