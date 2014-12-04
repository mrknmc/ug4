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
        if post['PostTypeId'] == '2' and 'OwnerUserId' in post:
            yield post


for owner, posts in groupby(parse(sys.stdin), key=itemgetter('OwnerUserId')):
    # prints OwnerUserId <TAB> Q1_ID <TAB> Q2_ID ...
    print('{0}\t{1}'.format(owner, '\t'.join(post['ParentId'] for post in posts)))

