#! /usr/bin/env python
import dtw
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
mpl.rc('font', family='serif', size=11)
mpl.rc('savefig', bbox='tight')







def run_dtw(t, x, y, xname=None, yname=None, offset=0, vmax=None):
  dist, dist_mat, cost, path = dtw.dtw(x[:,np.newaxis], y[:,np.newaxis])
  fig = plt.figure(figsize=(24, 6))
  plt.subplot(131)
  plt.plot(t, x, c='purple', label='x')
  plt.plot(t, y, c='green', label='y')
  plt.legend(loc=0)
  plt.xlabel('time')
  plt.ylabel('value')
  plt.subplot(132)
  cost1 = dist_mat[1:, 1:]
  offset = t[0]
  extent = (offset, offset+cost1.shape[1], offset, offset+cost1.shape[0])
  plt.imshow(cost1[::-1], cmap='viridis', extent=extent, vmin=0.0, vmax=vmax)
  plt.axis(extent)
  plt.xticks(np.asarray(np.linspace(extent[0], extent[1], 5), int))
  plt.yticks(np.asarray(np.linspace(extent[2], extent[3], 5), int))
  cb = plt.colorbar()
  cb.set_label('Dist', rotation=-90, va='bottom')
  plt.xlabel('x')
  plt.ylabel('y')
  plt.subplot(133)
  cost1 = cost[1:, 1:]
  offset = t[0]
  extent = (offset, offset+cost1.shape[1], offset, offset+cost1.shape[0])
  plt.imshow(cost1[::-1], cmap='viridis',extent=extent, vmin=0.0, vmax=vmax)
  w = offset + path
  plt.plot(w[1], w[0], 'w-')
  plt.axis(extent)
  plt.xticks(np.asarray(np.linspace(extent[0], extent[1], 5), int))
  plt.yticks(np.asarray(np.linspace(extent[2], extent[3], 5), int))
  cb = plt.colorbar()
  cb.set_label('Cost', rotation=-90, va='bottom')
  plt.xlabel('x')
  plt.ylabel('y')
  #fname = 'cost-{0}-to-{1}'.format(make_fname_safe(xname), make_fname_safe(yname))
  plt.savefig('name.png')
  plt.savefig('name.eps')
  print('Warping between {0} and {1}:'.format(xname, yname))
  print('  Distance is ', dist)

def read_info(info):
  list = info.split(',')
  a = np.empty(len(list))
  for u in range(len(list)):
    a[u] = float(list[u])
  return a

def read_class_file(filename):
  global class_time
  global class_in
  global class_out


  file = open(filename, "r")
  for line in file.readlines():
    line_hd,line_def = line.split(',',1)
    if line_hd == "time": class_time = read_info(line_def)
    if line_hd == "In": class_in = read_info(line_def)
    if line_hd == "Out": class_out = read_info(line_def)

def read_cyclus_file(filename):
  global cyclus_time
  global cyclus_in
  global cyclus_out


  file = open(filename, "r")
  lines = file.readlines()
  l = len(lines) -1

  cyclus_time  = np.lc(l)
  cyclus_in    = np.empty(l)
  cyclus_out   = np.empty(l)

  i = 0
  for line in lines[1:]:
    time,c_in,c_out,tmp = line.split(',')
    cyclus_time[i] = float(time)/12.
    cyclus_in[i] = float(c_in)
    cyclus_out[i] = float(c_out)
    i = i+1





def main():
  read_class_file("reactor_cumul.dat")
  read_cyclus_file("cyclus_reactor_cumul.csv")

  print(len(class_time[:-1]))
  print(len(class_in[:-1]))
  print(len(cyclus_in))

  run_dtw(cyclus_time, class_out[:-1], cyclus_out)


main()