import numpy as np
import numpy_indexed as npi
import copy

def ndims(X):
  return np.array(list(X.keys())).shape[1]

def norm(X):
  return np.linalg.norm(list(X.values()))

def size(X):
  idx = np.array(list(X.keys()))
  max_idx = np.max(idx,axis=0)
  data_shape = list(map(lambda x: x+1,max_idx))
  return data_shape

def mttkrp(X,U,mode,R,N):
  V = np.zeros((size(X)[mode],R))
  for r in range(R):
    X_new = copy.deepcopy(X)
    for n in range(N):
      if n != mode:
        for indices in X:
          X_new[indices] = X_new[indices] * U[n][:,r][indices[n]]
    X_array = []
    for k,v in X_new.items():
      tmp = list(k)
      tmp.append(v)
      #tmp.extend(v)
      X_array.append(tmp)
    X_array = np.array(X_array)
    V[:,r] = npi.group_by(X_array[:,mode]).sum(X_array[:,-1])[1]
  return V


def kruskal_norm(U,lamb,N):
  #coefMatrix = lamb@lamb.T
  lamb = lamb[0]
  coefMatrix = np.outer(lamb,lamb)
  for i in range(N):
    coefMatrix = coefMatrix * (U[i].T@U[i])
  nrm = np.sqrt(abs(np.sum(coefMatrix)))
  return nrm

def kruskal_innerprod(X,U,lamb,R,N):
  lamb = lamb[0]
  res = 0
  for r in range(R):
    X_new = copy.deepcopy(X)
    for n in range(N):
      for indices in X:
        X_new[indices]  = X_new[indices] * U[n][:,r][indices[n]]
    ttv = np.sum(list(X_new.values()))
    res = res + lamb[r] * ttv
  return res



