# set terminal png
set terminal png transparent enhanced font 'arial,9' fontscale 1.0 size 400,240
set output "lists.png"
set key left top
set xlabel "Documents processed"
set ylabel "Sum of lengths of inverted lists (n)"
f(x) = m*x + b
fit f(x) 'lists.dat' using 1:2 via m,b
set xrange [0:10000]
plot "lists.dat" using 2 title 'n' lt rgb "gray", \
    f(x) title 'Line Fit' lt rgb "red"

# doc(x) = f(x) * log(f(x))
# term(x) = f(x) + 100000
# plot doc(x) title 'Doc at a time', \
#     term(x) title 'Term at a time'
