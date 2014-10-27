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

from models import Network, BaseStation, Node

INPUT_FILE = 'input.txt'
OUTPUT_FILE = 'log.txt'


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


def main():
    """"""
    min_budget, nodes, bcsts = parse_file(INPUT_FILE)
    network = Network(nodes, min_budget)
    bs = BaseStation(network)
    bs.start_discovery()


if __name__ == '__main__':
    main()
