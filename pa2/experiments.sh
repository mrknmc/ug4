#!/usr/bin/env bash

#################################
# STANDARD CONFIGURATION
#######################I##########

# MSI
python3 cache.py --metrics metrics.txt trace1.txt
python3 cache.py --metrics metrics.txt trace2.txt

# MESI
python3 cache.py --mesi --metrics metrics.txt trace1.txt
python3 cache.py --mesi --metrics metrics.txt trace2.txt

#################################
# NON-STANDARD CONFIGURATION
#######################I##########

words=[1,4,16,32,64,128,256]
lines=[1024]

for word in $words; do
    for line in $lines; do
        python3 cache.py trace1.txt
    done
done
