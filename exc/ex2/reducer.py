#!/usr/bin/python

import sys

prev_line = -1

for line in sys.stdin:
    if line != prev_line:
        print(prev_line)
        prev_line = line
