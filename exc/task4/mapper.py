#!/usr/bin/python

"""
hadoop jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar -input /user/s1140740/task_2.out -output /user/s1140740/task_4.out -mapper mapper.py -file mapper.py -reducer reducer.py -file reducer.py
"""

import sys

for line in sys.stdin:
    words = line.strip().split()
    for triple in (words[i:i+3] for i in range(len(words) - 2)):
        triple = ('{0!r}'.format(t) for t in triple)
        triple = ', '.join(triple)
        print('{0}\t{1}'.format(triple, 1))
