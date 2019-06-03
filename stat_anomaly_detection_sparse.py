import numpy as np
import math
#from decimal import *
from scipy.stats import poisson
from scipy import sparse
from functools import reduce

def first_step(X,N,R,orig_shape):

  lamb = np.loadtxt('/Users/kojimajun/MultiAspectSpotting/MATLAB/PTF_lambda.csv',delimiter=',')

  U = {}
  for n in range(N):
    U[n] = np.loadtxt('/Users/kojimajun/MultiAspectSpotting/MATLAB/PTF_mode'+str(n+1)+'.csv',delimiter=',')

  #Uをスパースに展開
  #Cr = {}
  for r in range(R):
    tmp = sparse.kron(sparse.csr_matrix(U[0][:,r],dtype=np.float32),sparse.csr_matrix(U[1][:,r],dtype=np.float32))
    for n in range(2,N):
      tmp1 = sparse.csr_matrix(U[n][:,r],dtype=np.float32)
      tmp2 = sparse.kron(tmp,tmp1)
    Cr = tmp2
    if r == 0:
      result = lamb[0]*Cr
    else:
      result = result + lamb[r]*Cr
  print('calc mu done.')

  #Xをスパースに展開
  sparse_key = 1
  for n in orig_shape:
    sparse_key = sparse_key * n
  row = []
  col = []
  data = []
  for indices in X:
    if X[indices] != 0:
      X_index = 0
      i = 0
      for n in reversed(indices):
        if i==0:
          times = 1
        elif i==1:
          times = orig_shape[-1*i]
        else:
          times = reduce(lambda x,y:x*y,orig_shape[-1*i:])
        X_index = X_index + n*times
        i = i + 1
      row.append(0)
      col.append(X_index)
      data.append(X[indices])
  X_sparse = sparse.coo_matrix((data,(row,col)),shape=(1,sparse_key),dtype=np.float32)
  X_sparse = X_sparse.tocsr()
  print('X sparse done.')

  #muとXをまとめる
  poi = np.zeros((sparse_key,3))
  tmp = sparse.vstack((X_sparse,result)).tocsr()
  cnt = 0
  for i,j in zip(*tmp.nonzero()):
    poi[j,i] = tmp[i,j]
    cnt += 1
    if cnt % 100000 == 0:
      print(cnt)
  print('X mu marge done.')

  #2:Poisson累積確率を求める
  for i,rows in enumerate(poi):
    poi[i,2] = poisson.cdf(int(rows[0]),rows[1])
  print('calc poisson done.')

  #3:anomaryscoreを求める
  anomaly_score = np.zeros((sparse_key,1))
  for i,rows in enumerate(poi):
    if rows[0] <= rows[1]:
      if rows[2] == 0:
        anomaly_score[i] = 0
      else:
        anomaly_score[i] = -1*np.log10(rows[2])
    else:
      if rows[2] == 1:
        anomaly_score[i] = 0
      else:
        anomaly_score[i] = -1*np.log10(1-rows[2])
  print('calc anomaly score done.')
  #anomaly_score = sparse.csr_matrix(anomaly_score)
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