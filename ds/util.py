import math


def distance(node1, node2):
    """Euclidean distance between two nodes."""
    dx = node1.coords.x - node2.coords.x
    dy = node1.coords.y - node2.coords.y
    return math.sqrt(dx * dx + dy * dy)
