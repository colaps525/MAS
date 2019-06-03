import numpy as np
import math
#from decimal import *
from scipy.stats import poisson

def first_step(X,N,R):

  lamb = np.loadtxt('/Users/kojimajun/MultiAspectSpotting/MATLAB/PTF_lambda.csv',delimiter=',')

  U = {}
  for n in range(N):
    U[n] = np.loadtxt('/Users/kojimajun/MultiAspectSpotting/MATLAB/PTF_mode'+str(n+1)+'.csv',delimiter=',')

  #1:μを求める
  mu = {}
  for indices in X:
    p_sum = 0
    for r in range(R):
      p = 1
      for n in range(N):
        p = p * U[n][:,r][indices[n]]
      p_sum = p_sum + lamb[r] * p
    mu[indices] = p_sum
  print('calc mu done.')

  #2:Poisson累積確率を求める
  F = {}
  for indices in X:
    #f_sum = 0
    #for k in range(int(X[indices])):
      #f = (np.power(mu[indices],k)/math.factorial(k))*np.power(math#.e,-1*mu[indices])
      #f_sum = f_sum + f
    f_sum = poisson.cdf(int(X[indices]),mu[indices])
    F[indices] = f_sum
  print('calc poisson done.')

  #3:anomaryscoreを求める
  delta = 0.000000000000001
  anomaly_score = {}
  for indices in X:
    if X[indices] <= mu[indices]:
      if F[indices] == 0:
        F[indices] = F[indices] + delta
      anomaly_score[indices] = -1*np.log10(F[indices])
    else:
      if F[indices] == 1:
        F[indices] = F[indices] - delta
      anomaly_score[indices] = -1*np.log10(1-F[indices])
  print('calc anomaly score done.')

  return anomaly_score


if __name__ == '__main__':
  X = {}
  X[(4,0,0)] = 1
  X[(2,0,1)] = 1
  X[(0,0,2)] = 1
  X[(1,0,2)] = 1
  X[(3,0,2)] = 1
  X[(5,0,2)] = 1
  X[(0,0,3)] = 1
  X[(1,0,3)] = 1
  X[(3,0,3)] = 1
  X[(5,0,3)] = 1
  X[(0,1,0)] = 1
  X[(2,1,0)] = 1
  X[(4,1,0)] = 1

  N = 3
  R = 2
  B = first_step(X,N,R)

  print(B)