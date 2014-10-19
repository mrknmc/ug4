
best = set(open('pairs3.out'))
ref = set(open('pairs2.out'))
print(len(ref & best) / float(len(best | ref)))
