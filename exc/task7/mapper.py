#!/usr/bin/python

"""
hadoop jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar \
    -input /user/s1250553/ex1/matrixSmall.txt \
    -output /user/s1140740/task7/output \
    -mapper mapper.py \
    -file mapper.py \
    -reducer reducer.py \
    -file reducer.py \
    -jobconf stream.map.output.field.separator=, \
    -jobconf stream.num.map.output.key.fields=2 \
    -jobconf map.output.key.field.separator=, \
    -jobconf num.key.fields.for.partition=1 \
"""

import sys

matrix = []

for line in sys.stdin:
    row_no, col_vals = line.strip().split('\t')
    col_vals = col_vals.split()
    for col_no, col_val in enumerate(col_vals):
        if col_no == len(matrix):
            matrix.append((row_no, [col_val]))
        else:
            matrix[col_no][1].append(col_val)

for col_no, (row_no, col_vals) in enumerate(matrix):
    col_str = ' '.join(col_vals)
    print('{0},{1},{2}'.format(col_no, row_no, col_str))
