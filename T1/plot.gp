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
set output 'Storage_U8_UnBatched.png';
set key width 2

plot '/Users/mouginot/work/OFCB/cyclus/input/OFCB/1/UnBatched/Output.dat' \
          using 1:8 title 'CYCLUS' with lines,\
      '/Users/mouginot/work/OFCB/CLASS_calculation/1/ReadRootOuput.dat' \
          using 1:8 title 'CLASS\_BaM' with lines,\
     '/Users/mouginot/work/OFCB/CLASS_BENCH/reactors/test1/data/bench_uox_test01.tab'\
          using 1:24 title 'CLASS' with lines



set output 'Storage_U8_Batched.png';
plot '/Users/mouginot/work/OFCB/cyclus/input/OFCB/1/Batched/Output.dat' \
          using 1:8 title 'CYCLUS' with lines,\
     '/Users/mouginot/work/OFCB/CLASS_BENCH/reactors/test1/data/bench_uox_test01.tab'\
          using 1:24 title 'CLASS' with lines

#****************************************************************
