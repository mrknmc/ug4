set terminal png transparent enhanced fontscale 1.0 size 600,300
set output "results.png"
set key left top
set xlabel "Number of documents"
set logscale y
set ylabel "Running time (seconds)"
set auto x
plot "results.dat" using 2:xtic(1) title 'brute.py' with lines lt rgb "red", \
    '' using 3:xtic(1) title 'index.py' with lines lt rgb "blue", \
    '' using 4:xtic(1) title 'best.py' with lines lt rgb "green",
