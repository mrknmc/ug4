#!/usr/bin/env python2.7

import sys
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


for post in parse(sys.stdin):
    if post['PostTypeId'] == '2':
        # answer
        print('{0} {1}\t{2}\t{3}'.format(post['ParentId'], post['PostTypeId'], post['Id'], post['OwnerUserId']))
    else:
        # question
        print('{0} {1}\t{2}'.format(post['Id'], post['PostTypeId'], post['AcceptedAnswerId']))

