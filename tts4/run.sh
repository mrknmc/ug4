#!/usr/bin/env bash

python graph.py
neato -Tpng graph.dot > graph.png
open graph.png
