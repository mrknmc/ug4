#!/usr/bin/env bash

diff <(cat type1.truth | sort) <(cat type1.dup | sort) -U 0

diff <(cat type2.truth | sort) <(cat type2.dup | sort) -U 0
