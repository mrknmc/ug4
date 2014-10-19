#!/usr/bin/python

"""
hadoop jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar \
    -input /user/s1140740/ex2/input \
    -output /user/s1140740/ex2/output \
    -mapper mapper.py \
    -file mapper.py \
    -reducer reducer.py \
    -file reducer.py
"""

import sys

for line in sys.stdin:
    print(line.strip().lower())
