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
        for idx, line in enumerate(pr):
            rank, email = line.split()
            if idx < 10:
                rank = float(rank)
                G.add_node(email, {'rank': rank, 'shape': 'box'})

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

    reverse_emails = {}

    # create edges between people who sent emails
    with open('graph.txt') as graph:
        outs = defaultdict(lambda: defaultdict(set))

        for line in graph:
            email_id, sender, receiver = line.split()
            if sender in G and receiver in G and sender != receiver:
                reverse_emails[email_id] = sender, receiver
                outs[sender][receiver].add(email_id)

        for idx, (sender, data) in enumerate(outs.items(), start=1):
            for receiver, emails in data.items():
                # take a log to scale
                G.add_edge(
                    sender, receiver,
                    taillabel=len(emails),
                    color='gray30',
                    fontcolor='crimson',
                    labelfontsize=18
                )

    nx.write_dot(G, 'graph.dot')

if __name__ == '__main__':
    main()
