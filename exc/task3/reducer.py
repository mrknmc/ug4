#!/usr/bin/python

import sys

words_total = 0
line_total = 0

for line in sys.stdin:
    line = line.strip()
    line, words = line.split()
    words_total += int(words)
    line_total += int(line)

print('{} {}'.format(line_total, words_total))
