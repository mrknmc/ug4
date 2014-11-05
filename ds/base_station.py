from util import log, Event


def start_discovery(network):
    """Tell nodes to discover neighbours."""
    for node in network:
        node.discover(network)
    return network


def find_mst(network):
    """Perform next level of the algorithm."""
    # at first every node is a leader
    leaders = set(network)
    while len(leaders) > 1:
        log(Event.BS, leaders)
        min_edges = set(ldr.lead(network) for ldr in leaders)
        log(Event.ADDED, min_edges)
        for leader in leaders:
            leader.merge(network, leader.id)
        # new leaders are going to be a subset of previous leaders
        leaders = set(ldr for ldr in leaders if ldr.leader_id == ldr.id)
        log(Event.ELECTED, leaders)

    log(Event.BS, leaders)
    return network
