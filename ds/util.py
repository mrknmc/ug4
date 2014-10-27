import math


def distance(node1, node2):
    """Euclidean distance between two nodes."""
    dx = node1.x - node2.x
    dy = node1.y - node2.y
    return math.sqrt(dx * dx + dy * dy)
