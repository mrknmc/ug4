#!/usr/bin/python

import sys
import json

prev_student_id = None
prev_student = {}


def print_student(student):
    """Prints out a student."""
    # create strings for courses
    course_strs = []
    for course_id, mark in student['courses'].iteritems():
        course_str = '({0}, {1})'.format(course_id, mark)
        course_strs.append(course_str)

    # join course strings into one
    out_str = '{0} --> {1}'.format(student['name'], ' '.join(course_strs))
    print(out_str)


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

    # print and clear previous student if student changed
    if prev_student_id is not None and prev_student_id != student_id:
        print_student(prev_student)
        prev_student = {}
    else:
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

# print the last student
print_student(prev_student)
