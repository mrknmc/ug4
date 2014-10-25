#!/usr/bin/python

"""
hadoop jar /opt/hadoop/hadoop-0.20.2/contrib/streaming/hadoop-0.20.2-streaming.jar -input /user/s1250553/ex1/uniLarge.txt -output /user/s1140740/task_8.out -mapper mapper.py -file mapper.py -reducer reducer.py -file reducer.py
"""

import sys
import json

students = {}

for line in sys.stdin:
    type_, rest = line.strip().split('   ', 1)
    if type_ == 'student':
        student_id, name = rest.split('   ')
    else:
        course_id, student_id, mark = rest.split('   ')

    # create student dict if not exists
    student = students.setdefault(student_id, {})
    # update name if not exists
    student.setdefault('name', None)
    # update course dict if not exists
    courses = student.setdefault('courses', {})

    if type_ == 'student':
        # update name if known
        student['name'] = name
    else:
        # update mark if known
        courses[course_id] = mark

for stud_id, student in students.iteritems():
    # output name only if known
    name = student['name']
    name = '\t{0}'.format(name) if name is not None else ''
    courses = json.dumps(student['courses'])
    out_str = '{0}{1}\t{2}'.format(stud_id, name, courses)
    print(out_str)
