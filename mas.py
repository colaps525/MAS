from stat_anomaly_detection import first_step
from set_binary_tensor import set_binary_tensor
from densespot import densespot
from sparse_tensor_utils import size
import pandas as pd

df_id = pd.read_csv('/Users/kojimajun/MultiAspectSpotting/result_edit_anno_id_for_python_port003.csv')
#df_id = pd.read_csv('/Users/kojimajun/MultiAspectSpotting/MATLAB/old/test.csv')
dim_cols = ['src_ip','dst_ip','dst_port']
value_col = ['num']
X = {}
for index,row in df_id.iterrows():
  dim_id = []
  for d in dim_cols:
    dim_id.append(int(row[d]))
  dim_id = tuple(dim_id)
  X[dim_id] = float(row[value_col])


data_shape = size(X)
N = 3
#R = 2
R=10

#1:anomaly_scoreの計算
anomaly_score = first_step(X,N,R)

#2:バイナリテンソルの作成
t = 10.0
B1 = set_binary_tensor(anomaly_score,t)

#3:DenseSpotの実行
#S = 2
S=20
d = 10
C_min = densespot(B1,S,d,N,R,data_shape)
#print(C_min)

#4:インデックスを求める
rows, cols = C_min.nonzero()
re_index = []
for col in cols:
  idx = []
  for i,n in enumerate(reversed(data_shape)):
    if i == 0:
      q, mod = divmod(col,n)
      idx.append(mod)
    else:
      q, mod = divmod(q,n)
      idx.append(mod)
  re_index.append(list(reversed(idx)))
print(re_index)


