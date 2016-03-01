#! /usr/bin/env python
import dtw
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
mpl.rc('font', family='serif', size=11)
mpl.rc('savefig', bbox='tight')

import george
import george.kernels
from george.kernels import ExpSquaredKernel
import scipy.optimize as op


# Set up the Gaussian process.
def init_gp(t, y, yerr):
  y_mean = np.mean(y)
    kernel = float(y_mean) * ExpSquaredKernel(1.0)
    gp = george.GP(kernel, mean=y_mean)
    gp.compute(t, yerr=yerr, sort=False)
    return gp

def negloglikelihood(gp, y, hyperparams):
  gp.kernel[:] = hyperparams
    ll = gp.lnlikelihood(y, quiet=True)
    return -ll if np.isfinite(ll) else 1e25  # mask infinites

def grad_negloglikelihood(gp, y, hyperparams):
  gp.kernel[:] = hyperparams
    gll = gp.grad_lnlikelihood(y, quiet=True)
    #gll[~np.isfinite(gll)] = 0.0
    return -gll

def optimize_hyperparams(gp, y):
  hp0 = gp.kernel.vector
    # form some closures
    nll = lambda hp: negloglikelihood(gp, y, hp)
    grad_nll = lambda hp: grad_negloglikelihood(gp, y, hp)
    results = op.minimize(nll, hp0, jac=grad_nll)
    gp.kernel[:] = results.x

def model(t, y, tstar, yerr=1e-6):
  gp = init_gp(t, y, yerr)
    optimize_hyperparams(gp, y)
    mu, cov = gp.predict(y, tstar)
    std = np.sqrt(np.diag(cov))
    return mu, std, gp


def model_plot(t, y, yerr, tpred, mu, std, title=None, ymax=None, show_title=True):
  fig = plt.figure(figsize=(8, 8))
    T = len(t) / 2
    plt.errorbar(t[:T], y[:T], yerr if yerr is None else yerr[:T], fmt='r.', label='DYMOND')
    plt.errorbar(t[T:], y[T:], yerr if yerr is None else yerr[T:], fmt='rx', label='Cyclus')
    plt.plot(tpred, mu, 'k-', label='model')
    plt.fill_between(tpred, mu - 2*std, mu + 2*std, color='gray')
    ax = plt.axis()
    plt.axis([tpred[0], tpred[-1], 0.0, ymax or ax[3]])
    plt.xticks(np.linspace(tpred[0], tpred[-1], 5))
    plt.legend(loc=0)
    plt.xlabel('Time [year]')
    plt.ylabel('Generated Power [GWe]')
    if title and show_title:
      plt.title(title)
    fbase = 'gwe-model-' + (title or '').lower().replace(' ', '-')
    plt.savefig(fbase + '.eps')
    plt.savefig(fbase + '.png')






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

  cyclus_time  = np.empty(l)
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

  run_dtw(cyclus_time, class_in[:-1], cyclus_in)


main()