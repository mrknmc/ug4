import math

from contextlib import nested
from collections import defaultdict


def parse(f):
    """Parses input file and creates a graph representation."""
    ins = defaultdict(lambda: defaultdict(int))
    outs = defaultdict(lambda: defaultdict(int))
    people = set()
    for idx, line in enumerate(f):
        email_id, sender, receiver = line.split()
        if sender != receiver:
            # don't include self-emails
            people.add(sender)
            people.add(receiver)
            ins[receiver][sender] += 1
            outs[sender][receiver] += 1
    return people, outs, ins


def out(outs, sender):
    """Computes the out degree of a sender."""
    return sum(outs[sender].values())


def sink_sum(probs, outs):
    """Sum of probabilities over sink nodes."""
    return sum(prob for person, prob in probs.items() if out(outs, person) == 0)


def page_rank(people, outs, ins, iters, lmb=0.8):
    """PageRank algorithm"""
    # initialize to 1/N
    people_count = len(people)
    probs = {person: 1.0 / people_count for person in people}
    new_probs = {}

    for i in range(iters):
        s = sink_sum(probs, outs)
        for p in people:
            rank = (1.0 - lmb + lmb * s) / people_count
            rank += lmb * sum(w * probs[s] / out(outs, s) for s, w in ins[p].items())
            new_probs[p] = rank
        probs, new_probs = new_probs, probs
    return probs


def normalize(dist):
    """Normalizes probability distributions so squares add to 1."""
    denom = math.sqrt(sum(prob * prob for prob in dist.values()))
    return {p: prob / denom for p, prob in dist.items()}


def hits(people, outs, ins, iters):
    """HITS algorithm."""
    denom = math.sqrt(len(people))
    hubs = {person: 1.0 / denom for person in people}
    auths = {person: 1.0 / denom for person in people}
    new_hubs = {}
    new_auths = {}

    print(hubs['jeff.dasovich@enron.com'])
    print(hubs['john.lavorato@enron.com'])
    print(auths['jeff.dasovich@enron.com'])
    print(auths['john.lavorato@enron.com'])

    for i in range(iters):
        for p in people:
            new_hubs[p] = sum(w * auths[rec] for rec, w in outs[p].items())
            new_auths[p] = sum(w * hubs[sen] for sen, w in ins[p].items())

        hubs, new_hubs = normalize(new_hubs), hubs
        auths, new_auths = normalize(new_auths), auths

        if i == 0:
            print(hubs['jeff.dasovich@enron.com'])
            print(hubs['john.lavorato@enron.com'])
            print(auths['jeff.dasovich@enron.com'])
            print(auths['john.lavorato@enron.com'])
    return hubs, auths


def log(f, dist, n=100):
    """Writes n emails with highest scores to a file."""
    for (email, score) in sorted(dist.items(), key=lambda x: -x[1])[:n]:
        f.write('{0:.6f} {1}\n'.format(score, email))


def main():
    """"""
    with nested(
        open('graph.txt'),
        open('hubs.txt', 'w'),
        open('auth.txt', 'w'),
        open('pr.txt', 'w'),
    ) as (f, h, a, pr):
        people, outs, ins = parse(f)
        # pranks = page_rank(people, outs, ins, 10)
        # log(pr, pranks)
        hubs, auths = hits(people, outs, ins, 10)
        log(h, hubs)
        log(a, auths)


if __name__ == '__main__':
    main()
