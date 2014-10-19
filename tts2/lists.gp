set terminal png transparent enhanced fontscale 1.0 size 600,300
set output "lists.png"
set key left top
set xlabel "Number of documents"
set ylabel "Sum of lengths of inverted lists (n)"
f(x) = m*x + b
fit f(x) 'lists.dat' using 1:2 via m,b
set xrange [0:10000]
plot "lists.dat" using 2 title 'n' lt rgb "gray", \
    f(x) title 'Line Fit' lt rgb "red"
