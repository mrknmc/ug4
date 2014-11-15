import math
import re
import networkx as nx
import matplotlib

from collections import defaultdict

matplotlib.rc('font', family='DejaVu Sans')


def main():
    """"""
    G = nx.DiGraph(
        overlap=False,
        splines=True,
        sep=1,
    )

    # take first 10 peeps with highest PR
    with open('pr.txt') as pr:
        total_rank = 0.0
        for idx, line in enumerate(pr):
            rank, email = line.split()
            if idx < 10:
                rank = float(rank)
                total_rank += rank
                G.add_node(email, {'rank': rank, 'shape': 'box'})

    # size is their PR / total
    for (node, data) in G.nodes(data=True):
        G.node[node]['ratio'] = data['rank'] / total_rank

    unames2emails = dict((node.split('@', 1)[0], node) for node in G.nodes())

    # add their attributes
    with open('roles.txt') as roles:
        for line in roles:
            a = re.split(r'(\t|  +)', line)
            a = [b.strip() for b in a]
            a = a + [None] * (7 - len(a))
            uname, _, name, _, role, _, company = a
            if uname in unames2emails:
                email = unames2emails[uname]
                if name is not None:
                    G.node[email]['label'] = '\n'.join([email, name])
                if role is not None:
                    G.node[email]['label'] = '\n'.join([email, name, role])
                if company is not None:
                    G.node[email]['label'] = '\n'.join([email, name, role, company])

    # create edges between people who sent emails
    with open('graph.txt') as graph:
        outs = defaultdict(lambda: defaultdict(set))

        for line in graph:
            email_id, sender, receiver = line.split()
            if sender in G and receiver in G and sender != receiver:
                outs[sender][receiver].add(email_id)

        for idx, (sender, data) in enumerate(outs.items(), start=1):
            for receiver, emails in data.items():
                G.add_edge(sender, receiver)

    nx.write_dot(G, 'graph.dot')
    # G = nx.convert_node_labels_to_integers(G)

    # print(nx.get_node_attributes(G, 'ratio').values())

    # nx.draw_circular(
    #     G,
    #     node_size=[size * 100000 for size in nx.get_node_attributes(G, 'ratio').values()],
    #     # with_labels=True
    # )
    # plt.show()

if __name__ == '__main__':
    main()
