from collections import defaultdict


def parse(f):
    """"""
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


def main():
    """"""
    with open('graph.txt') as f:
        people, outs, ins = parse(f)
        probs = page_rank(people, outs, ins, 10)
        for tup in sorted(probs.items(), key=lambda x: -x[1])[:10]:
            print(tup)


if __name__ == '__main__':
    main()
