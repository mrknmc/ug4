from util import log
from models import Event


def broadcast(node_id, network):
    """Starts a broadcast at a node."""
    network.get(node_id).broadcast()
    return network


def start_discovery(network):
    """Tell nodes to discover neighbours."""
    for node in network:
        node.discover(network)
    return network


def find_mst(network):
    """Perform next level of the algorithm."""
    # at first every node is a leader
    leaders = set(network)
    log(Event.BS, *leaders)
    while 1:
        min_edges = set(ldr.lead(network) for ldr in leaders)

        for leader in leaders:
            leader.merge(network, leader.id)

        # new leaders are going to be a subset of previous leaders
        new_leaders = set(ldr for ldr in leaders if ldr.is_leader)
        if new_leaders == leaders:
            break

        leaders = new_leaders
        min_edges.discard(None)  # ignore None responses
        log(Event.ADDED, *min_edges)
        log(Event.ELECTED, *leaders)
        log(Event.BS, *leaders)

    return network
