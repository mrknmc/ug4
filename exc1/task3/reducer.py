#!/usr/bin/python

import sys

words_total = 0
line_total = 0

for line in sys.stdin:
    line, words = line.strip().split()
    words_total += int(words)
    line_total += int(line)

print('{0} {1}'.format(line_total, words_total))
