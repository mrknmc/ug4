#!/usr/bin/python

"""
hadoop jar contrib/streaming/hadoop-0.20.2-streaming.jar \
    -input /user/s1250553/ex1/webSmall.txt \
    -output /user/s1140740/ex1/output \
    -mapper mapper.py \
    -file mapper.py
"""

import sys

for line in sys.stdin:
    print(line.lowercase())
