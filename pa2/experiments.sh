#! /bin/zsh

#################################
# STANDARD CONFIGURATION
#################################

echo -e "file,protocol,hit_rate,lines,words,total,hits,invalidations,shared_access,private_access,S->M,E->M" > metrics.csv

# MSI
# python3 cache.py --metrics metrics.csv trace1.txt
# python3 cache.py --metrics metrics.csv trace2.txt

# MESI
# python3 cache.py --mesi --metrics metrics.csv trace1.txt
# python3 cache.py --mesi --metrics metrics.csv trace2.txt

#################################
# NON-STANDARD CONFIGURATION
#################################

words=(1 4 16 32 64)
lines=(64 128 256 1024 4096)

echo -e "file,protocol,hit_rate,lines,words,total,hits,invalidations,shared_access,private_access,S->M,E->M" > $2

for word in $words; do
    for line in $lines; do
        echo -e "Running with $word words per line and $line lines per cache"
	python3 cache.py $1 --words $word --lines $line --metrics $2 $3 
    done
done
