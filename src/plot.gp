reset
load '~/.gnuplot'
unset key

file='../out.dat'
file1='../temp.dat'

binwidth=0.001
set boxwidth binwidth
bin(x,width)=width*floor(x/width)+width/2.0

set ylabel "Counts / 0.001"
set xlabel "Energy (arb)"
set terminal wxt 0
plot file u (bin($1,binwidth)):(1.0/binwidth) smooth freq w steps t 'Amplitude'
set terminal wxt 1
plot file u (bin($2,binwidth)):(1.0/binwidth) smooth freq w steps t 'Filter'

set terminal wxt 2
plot file1 

#set terminal postscript eps enhanced color solid "Helvetica, 24"
#set output '../pics/gaussTest.eps'
#replot