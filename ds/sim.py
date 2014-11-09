"""
1. The base­station alerts all the nodes to start constructing the MST
2. Each node discovers the other nodes in its proximity
3. The leader of a connected component broadcasts a message inside the component for
each node to identify a new edge to add to the MST
4. Each node chooses the link with the lowest weight to add, and sends it to the leader of its
component in a convergecast
5. The leader of a component chooses which link to add and broadcasts (floods in the tree)
its decision.
6. Once all the leaders have made their decisions, the beacon broadcasts a "merge"
message. All the leaders now flood (in the tree) their id, and in each connected component,
    the leader with the highest id becomes the leader of the entire component for the next level.
7. The base­station waits for all the components to finish before moving to the next level and
    broadcasts a beacon to start next level
8. The next level starts again from step 3.
9. The algorithm finishes when there is no mode link added to the MST in a level.
"""

import sys

from models import Network
from node import Node
from util import log
from base_station import start_discovery, find_mst


INPUT_FILE = 'input.txt'


def parse_file(path):
    """Parse the input file."""
    with open(path) as input_file:
        min_budget = float(next(input_file))
        bcsts = []
        nodes = []
        for line in input_file:
            if line.startswith('node'):
                node_id, x, y, energy = line.split(', ')
                node_id = int(node_id.lstrip('node '))
                node = Node(node_id, float(x), float(y), float(energy))
                nodes.append(node)
            else:
                bcst = line.lstrip('bcst from ')
                bcsts.append(bcst)
    return min_budget, nodes, bcsts


def main(input_file):
    """Main function of the simulator."""
    min_budget, nodes, bcsts = parse_file(input_file)
    network = Network(nodes, min_budget)
    network = start_discovery(network)
    network = find_mst(network)
    for node_id in bcsts:
        broadcast(node_id, network)


if __name__ == '__main__':
    input_file = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE
    log('Running simulator with file: {}.'.format(input_file))
    main(input_file)
