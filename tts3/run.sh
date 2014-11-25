#!/usr/bin/env bash

bits=(128);
ks=(8 16 32)

for bit in ${bits[@]}; do
    for k in ${ks[@]}; do
        echo -e "BITS: ${bit} \t k: ${k}"
        python2.6 detector.py $bit $k
        echo -e "\nTYPE 1:"
        diff <(cat type1.truth | sort) <(cat type1.dup | sort) | diffstat
        echo -e "\nTYPE 2:"
        diff <(cat type2.truth | sort) <(cat type2.dup | sort) | diffstat
        echo -e "\n"
    done
done
