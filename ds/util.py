import math


def distance(coords1, coords2):
    """Euclidean distance between two nodes."""
    dx = coords1.x - coords2.x
    dy = coords1.y - coords2.y
    return math.sqrt(dx * dx + dy * dy)
