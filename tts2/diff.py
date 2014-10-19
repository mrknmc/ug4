
best = set(open('pairs3.out'))
ref = set(open('pairs.ref'))
print(len(ref & best) / float(len(best | ref)))
