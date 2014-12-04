#!/usr/bin/env python2.7

import sys
import io
import xml.etree.ElementTree as ET


def make_post(serial):
    root = ET.fromstring(serial)
    return root.attrib


for line in sys.stdin:
    post = make_post(line.strip())
    if post['PostTypeId'] == '1':
        # is a question
        print('{0}\t{1}'.format(post['Id'], post['ViewCount']))

