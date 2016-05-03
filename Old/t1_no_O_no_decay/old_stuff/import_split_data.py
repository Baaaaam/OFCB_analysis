#!/usr/bin/env python
import numpy as np


def read(filename):
  my_file = open(filename, 'r')
  f_data = my_file.readlines()

  #get header
  col_header = f_data[0].split()
  n_col = len(col_header)

  #prepare data numpy
  data = []
  for i in range(n_col):
    data_ = []
    data.append(data_)
  #fill data numpy
  for line in f_data[1:]:
    words = line.split()
    for i in range(len(words)):
      data[i].append(float(words[i]))

  return col_header,data

def main():
  
  head,data= read("/Users/mouginot/work/OFCB/CLASS_BENCH/reactors/test1/data/bench_uox_test01.tab")
  total_r = []
  for t in range(len(data[0])):
    total = 0
    total_ma = 0
    for i in range(len(head)):
      if(head[i].find('REACTOR') >= 0):
        if(head[i].find('92000') >= 0 ):
          total += data[i][t]
        if(head[i].find('94000') >= 0 ):
          total += data[i][t]
        if(head[i].find('AM') >= 0 ):
          total += data[i][t]
        if(head[i].find('PF') >= 0 ):
            total += data[i][t]
      total_r.append(total)

  file = open("TEST.dat","w")
  file.write("Time R_total")



  for i in range(len(head)):
    print(head[i])

main()

#or head[i].find('PF') >= 0