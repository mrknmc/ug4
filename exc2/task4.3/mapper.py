#!/usr/bin/env python3

import sys
import io
import xml.etree.ElementTree as ET

from itertools import groupby
from operator import itemgetter


def make_post(serial):
    root = ET.fromstring(serial)
    return root.attrib


def parse(stream):
    for line in stream:
        post = make_post(line.strip())
        # sometimes answers do not have owner id
        if (post['PostTypeId'] == '2' and 'OwnerUserId' in post) or (post['PostTypeId'] == '1' and 'AcceptedAnswerId' in post):
            yield post


# make sure utf-8 encoding is used
input = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8') 
for post in parse(input):
    if post['PostTypeId'] == '2':
        # answer
        print('{0}\t{1}\t{2}\t{3}'.format(post['ParentId'], post['PostTypeId'], post['Id'], post['OwnerUserId']))
    else:
        # question
        print('{0}\t{1}\t{2}'.format(post['Id'], post['PostTypeId'], post['AcceptedAnswerId']))

