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
                label = '\n'.join(['PR: {}'.format(rank), email])
                G.add_node(email, {'rank': rank, 'shape': 'box', 'label': label})

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
                labels = []
                if name is not None:
                    labels.append(name)
                if role is not None:
                    labels.append(role)
                if company is not None:
                    labels.append(company)
                G.node[email]['label'] += '\n' + '\n'.join(labels)

    reverse_emails = {}

    # read subjects
    subjects = {}
    with open('subject.txt') as sub:
        for line in sub:
            email_id, subject = line.split(' ', 1)
            tokens = subject.split()
            subjects[email_id] = tokens

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
                weight = len(emails)
                if weight < 2:
                    continue

                tokens = []
                for email in emails:
                    tks = subjects[email]
                    tokens.extend(tks)

                token_counts = defaultdict(int)
                for token in tokens:
                    token = token.lower()
                    if token in ['re:', 'fw:', '&', 'to', 'of', '-', 'for', 'the', 'and']:
                        continue
                    token_counts[token] += 1

                top_3 = sorted(token_counts.items(), key=lambda x: -x[1])[:3]

                G.add_edge(
                    sender, receiver,
                    taillabel=weight,
                    color='gray30',
                    fontcolor='crimson',
                    labelfontsize=18,
                    label='[' + ', '.join(w[0] for w in top_3) + ']'
                )

    nx.write_dot(G, 'graph.dot')

if __name__ == '__main__':
    main()
