import numpy as np
from cp_als import cp_als
from scipy import sparse
import scipy.sparse.linalg as sp
from functools import reduce

def densespot(B1,S,d,N,R,orig_shape):
  C_hat,lamb = cp_als(B1,S)
  h = np.linspace(0.01, 0.1, d)
  #print(C_hat)
  C = {}
  for j in range(d):
    C[j] = {}
    for n in range(N):
      data_shape = C_hat[n].shape
      C[j][n] = np.zeros(data_shape)
   #   for s in range(S):
    for indices in B1:
      for s in range(S):
        prob = 1
        for n in range(N):
          prob = prob * C_hat[n][:,s][indices[n]]
        if prob >= h[j]:
          for n in range(N):
            C[j][n][:,s][indices[n]] = 1
  del C_hat

  #Bをスパースに変換
  sparse_key = 1
  for n in orig_shape:
    sparse_key = sparse_key * n
  row = []
  col = []
  data = []
  for indices in B1:
    if B1[indices] != 0:
      B_index = 0
      i = 0
      for n in reversed(indices):
        if i==0:
          times = 1
        elif i==1:
          times = orig_shape[-1*i]
        else:
          times = reduce(lambda x,y:x*y,orig_shape[-1*i:])
        B_index = B_index + n*times
        i = i + 1
      row.append(0)
      col.append(B_index)
      data.append(B1[indices])
  B_sparse = sparse.coo_matrix((data,(row,col)),shape=(1,sparse_key),dtype=np.int8)
  B_sparse = B_sparse.tocsr()

  #Cをテンソルに変換
  Cj = {}
  for j in range(d):
    for r in range(R):
      tmp = sparse.kron(sparse.csr_matrix(C[j][0][:,r],dtype=np.int8),sparse.csr_matrix(C[j][1][:,r],dtype=np.int8))
      for n in range(2,N):
        tmp1 = sparse.csr_matrix(C[j][n][:,r],dtype=np.int8)
        tmp2 = sparse.kron(tmp,tmp1)
      Cr = tmp2
      if r == 0:
        result = Cr
      else:
        result = result + Cr
    Cj[j] = result

  #最小のjを求める
  j_norm = []
  for j in range(d):
    diff = B_sparse-Cj[j]
    diff_power = diff.power(2)
    diff_sum = [diff_power[i,j] for i,j in zip(*diff_power.nonzero())]
    j_norm.append(np.sqrt(sum(diff_sum)))
  min_j_index = np.array(j_norm).argmin()
  print(j_norm)
  print(h[min_j_index])

  return Cj[min_j_index]
