from util import log, Event


def start_discovery(network):
    """Tell nodes to discover neighbours."""
    for node in network.nodes:
        node.discover(network)
    return network


def find_mst(network):
    """Perform next level of the algorithm."""
    # at first every node is a leader
    leaders = set(network.nodes)
    while len(leaders) > 1:
        log(Event.BS, *leaders)
        for leader in leaders:
            leader.lead()
        for leader in leaders:
            leader.merge()
        # new leaders are going to be a subset of previous leaders
        leaders = set(ldr for ldr in leaders if ldr.leader_id == ldr.id)

    log(Event.BS, *leaders)
    return network
