#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import io
import xml.etree.ElementTree as ET


def make_post(serial):
    root = ET.fromstring(serial)
    return root.attrib


# make sure utf-8 encoding is used
input = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8') 
for line in input:
    post = make_post(line.strip())
    if post['PostTypeId'] == '1':
        # is a question
        print('{0}\t{1}'.format(post['Id'], post['ViewCount']))

