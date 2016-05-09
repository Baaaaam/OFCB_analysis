#!/usr/bin/env gnuplot
#Header
set grid xtics ytics
show grid
set key center right noautotitle  box
set terminal png size 1000,750 enhanced font "Helvetica,20"
show xlabel
show ylabel

set xlabel "Time[y]"



#****************************************************************
set ylabel "Storage ^{238}U Inventory [tons]"
set term png;
set output 'Storage_U8.png';
set key width 2

plot '/Users/mouginot/work/OFCB/cyclus/input/OFCB/3/UnBatched/Output.dat' \
          using 1:8 title 'CYCLUS' with lines,\
     '/Users/mouginot/work/OFCB/CLASS_BENCH/reactors/test3/data/bench_uox_test03.tab'\
          using 1:24 title 'CLASS' with lines



set output 'Storage_U8_CLASS_t1x10_vs_t3.png';
plot '/Users/mouginot/work/OFCB/CLASS_BENCH/reactors/test1/data/bench_uox_test01.tab' \
          using 1:(10*$24) title '(CLASS\_t1)x2' with lines,\
     '/Users/mouginot/work/OFCB/CLASS_BENCH/reactors/test3/data/bench_uox_test03.tab' \
          using 1:24 title 'CLASS\_t2' with lines


set output 'Storage_U8_CYCLUS_t1x10_vs_t3.png';
plot '/Users/mouginot/work/OFCB/cyclus/input/OFCB/1/UnBatched/Output.dat' \
          using 1:(10*$8) title '(Cyclus\_t1)x2' with lines,\
     '/Users/mouginot/work/OFCB/cyclus/input/OFCB/3/UnBatched/Output.dat' \
          using 1:8 title 'Cyclus\_t2' with lines


set output 'Storage_U8_Batched.png';
plot '/Users/mouginot/work/OFCB/cyclus/input/OFCB/3/Batched/Output.dat' \
     using 1:8 title 'CYCLUS' with lines,\
     '/Users/mouginot/work/OFCB/CLASS_BENCH/reactors/test3/data/bench_uox_test03.tab'\
     using 1:24 title 'CLASS' with lines

#

#****************************************************************
