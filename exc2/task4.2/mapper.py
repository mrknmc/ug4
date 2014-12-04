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
        if post['PostTypeId'] == '2' and 'OwnerUserId' in post:
            yield post


# make sure utf-8 encoding is used
input = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8') 
for owner, posts in groupby(parse(input), key=itemgetter('OwnerUserId')):
    # prints OwnerUserId <TAB> Q1_ID <TAB> Q2_ID ...
    print('{0}\t{1}'.format(owner, '\t'.join(post['ParentId'] for post in posts)))

