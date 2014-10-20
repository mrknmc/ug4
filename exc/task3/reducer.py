#!/usr/bin/python

import sys

words_total = 0
line_total = 0

for line in sys.stdin:
    line = line.strip()
    words, line = line.split('\t')
    words_total += words
    line_total += line

print('{} {}'.format(line_total, words_total))
