#!/usr/bin/python

import sys

prev_col_no = None

for line in sys.stdin:
    col_no, row_no, col_str = line.strip().split(',')
    # not first column and column changed -> print \n
    if prev_col_no is not None and col_no != prev_col_no:
        # print('')
        print('\n{0}\t'.format(col_no)),
    elif prev_col_no is None:
        print('{0}\t'.format(col_no)),

    print(col_str),
    prev_col_no = col_no
