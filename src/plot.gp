reset
load '~/.gnuplot'
unset key

file='../out.dat'
#file='../temp.dat'

binwidth=0.001
set boxwidth binwidth
bin(x,width)=width*floor(x/width)+width/2.0

set ylabel "Counts / 0.001"
set xlabel "Energy (arb)"
plot file u (bin($2,binwidth)):(1.0/binwidth) smooth freq w steps t 'Singles'

#set terminal postscript eps enhanced color solid "Helvetica, 24"
#set output '../pics/gaussTest.eps'
#replot