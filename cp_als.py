import numpy as np
from sparse_tensor_utils import *

def cp_als(X,R):
  #TODO
  #Xが辞書型かどうか判定する


  #Extract number of dimensions
  #and norm of X
  N = ndims(X)
  normX = norm(X)
  data_shape = size(X)

  #Set algorithm parameters
  fitchangetol = 1e-4
  maxiters = 50
  dimorder = range(N)

  #Set up and error checking on initial guess for U
  #Observe that we don't need to calculate an initial guess for the
  # first index in dimorder because that will be solved
  #for in the first inner iteration.
  Uinit = {}
  Uinit[0] = np.array([])
  for n in range(1,N):
    Uinit[n] = np.random.rand(data_shape[n],R)
  #Uinit[1] =  np.loadtxt('/Users/kojimajun/MultiAspectForensics/MATLAB/test_U2_init.csv',delimiter=',',ndmin=2)
  #Uinit[2] =  np.loadtxt('/Users/kojimajun/MultiAspectForensics/MATLAB/test_U3_init.csv',delimiter=',',ndmin=2)

  U = Uinit
  fit = 0

  print('\nCP_ALS:\n')

  UtU = np.zeros((R,R,N))

  for n in range(N):
    if U[n].size != 0:
      UtU[:,:,n] = U[n].T@U[n]

  for iter in range(maxiters):
    fitold = fit

    #Iterate over all N modes of the tensor
    for n in dimorder:
      Unew = mttkrp(X,U,n,R,N)
      Y = np.prod([UtU[:,:,m] for m in range(N) if m!=n],axis=0)
      #Unew = Unew / Y
      Unew = np.dot(Unew, np.linalg.pinv(Y))

      if iter == 0:
        #列ごとの二乗和
        lamb = np.sqrt(np.sum(np.power(Unew,2),axis=0,keepdims=True))
      else:
        lamb = np.max(np.max(abs(Unew),axis=0,keepdims=True),axis=0,keepdims=True)
      Unew = Unew/lamb
      U[n] = Unew
      UtU[:,:,n] = U[n].T@U[n]

    normresidual = np.sqrt(np.power(normX,2) + np.power(kruskal_norm(U,lamb,N),2) - 2*kruskal_innerprod(X,U,lamb,R,N))
    fit = 1 - (normresidual / normX)

    fitchange = abs(fitold - fit)

    if (iter > 0) and (fitchange < fitchangetol):
      flag = 0
    else:
      flag = 1

    iter_msg = 'Iter %d: f= %f f-delta = %f\n' % (iter,fit,fitchange)
    print(iter_msg)

    if flag == 0:
      break

  for r in range(R):
    for n in range(N):
      tmp = np.linalg.norm(U[n][:,r])
      if tmp > 0:
        U[n][:,r] = U[n][:,r] / tmp
      lamb[0][r] = lamb[0][r] * tmp

  #debug

  lamb_idx = np.where(lamb[0] < 0)
  for idx in lamb_idx[0]:
    U[0][:,idx] = -1*U[0][:,idx]
    lamb[0][idx] = -1*lamb[0][idx]

  for r in range(R):
    max_val = []
    max_idx = []
    max_sign = []
    for n in range(N):
      max_val.append(np.max(abs(U[n][:,r])))
      max_idx.append(np.argmax(abs(U[n][:,r])))
      max_sign.append(int(np.sign(U[n][max_idx[n],r])))

    negidx = np.where(np.array(max_sign) == -1)
    nflip = int(2*np.floor(len(negidx[0])/2))
    for i in range(nflip):
      n = negidx[0][i]
      U[n][:,r] = -1*U[n][:,r]
  print(lamb)
  #np.savetxt('/Users/kojimajun/MultiAspectForensics/Python/tcpdump_test/05_test_result_cp_ip_src.csv',U[0],delimiter=',')
  #np.savetxt('/Users/kojimajun/MultiAspectForensics/Python/tcpdump_test/test_result_cp_ip_dst.csv',U[1],delimiter=',')
  #np.savetxt('/Users/kojimajun/MultiAspectForensics/Python/tcpdump_test/test_result_cp_dst_port.csv',U[2],delimiter=',')

  return U,lamb




if __name__ == '__main__':
  data = np.loadtxt('/Users/kojimajun/MultiAspectForensics/result_id.csv',delimiter=',',dtype=[('col1','int'),('col2','int'),('col3','int'),('col4','float')])
  X = {}
  for i in data:
    X[(i[0]-1,i[1]-1,i[2]-1)] = i[3]
  #3D
  #X[(0,0,0)] = 0.5
  #X[(0,0,2)] = 1.5
  #X[(0,1,0)] = 4.5
  #X[(1,1,0)] = 5.5
  #X[(1,1,1)] = 2.5
  #X[(2,2,3)] = 3.5

  #4D
  #X[(0,0,0,1)] = 0.5
  #X[(0,0,2,0)] = 1.5
  #X[(0,1,0,1)] = 4.5
  #X[(1,1,0,2)] = 5.5
  #X[(1,1,1,1)] = 2.5
  #X[(2,2,3,0)] = 3.5

  #print(X)

  #テストする
  #1,N=4次元にした場合
  #2,R=2以上にした場合
  cp_als(X,1)