#!/usr/bin/python

"""
hadoop jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar -input /user/s1140740/task_2.out -output /user/s1140740/task_3.out -mapper mapper.py -file mapper.py -reducer reducer.py -file reducer.py

hadoop dfs -cat /user/s1140740/task_3.out/* | awk '{ sum1 += $1; sum2 += $2 } END { print sum1, sum2 }'
"""

import sys

for line in sys.stdin:
    words = len(line.strip().split())
    print('{0} {1}'.format(1, words))