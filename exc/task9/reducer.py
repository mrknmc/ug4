#!/usr/bin/python

import sys
import json
import heapq

heap = []
prev_student_id = None
prev_student = {}


def add_student(heap, student):
    """Prints out a student."""
    # create strings for courses
    value = sum(mark in student['courses'].itervalues())
    heapq.heappush(heap, (-value, student['name']))


for line in sys.stdin:
    student_id, rest = line.strip().split('\t', 1)
    rest = rest.split('\t')
    if len(rest) == 2:
        # we have both name and courses
        name, courses = rest
    else:
        # we only have courses
        name, courses = None, rest[0]

    courses = json.loads(courses)

    # add and clear previous student if student changed
    if prev_student_id is not None and prev_student_id != student_id:
        add_student(heap, prev_student)
        prev_student = {}

    prev_student_id = student_id

    # set default values
    prev_student.setdefault('name', None)
    prev_student.setdefault('courses', {})

    # update name if not None
    if name is not None:
        prev_student['name'] = name

    # update course marks
    for course_id, mark in courses.iteritems():
        prev_student['courses'][course_id] = mark

# add the last student
add_student(heap, prev_student)


# print top students
prev_val = None
while 1:
    val, name = heapq.heappop(heap)
    val = -val
    if prev_val == val:
        print(name)
    elif prev_val is None:
        prev_val = val
    else:
        break
