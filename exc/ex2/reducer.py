#!/usr/bin/python

"""
hadoop jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar \
    -input /user/s1140740/ex2/input \
    -output /user/s1140740/ex2/output \
    -mapper cat \
    -reducer reducer.py \
    -file reducer.py
"""

import sys

prev_line = None

for line in sys.stdin:
    line = line.strip()
    if line != prev_line:
        if prev_line is not None:
            print(prev_line)
        prev_line = line

if prev_line == line:
    print(line)
