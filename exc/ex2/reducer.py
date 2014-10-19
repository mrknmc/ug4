#!/usr/bin/python

import sys

prev_line = None

for line in sys.stdin:
    if line != prev_line:
        if prev_line is not None:
            print(prev_line)
        prev_line = line

if prev_line == line:
    print(line)
