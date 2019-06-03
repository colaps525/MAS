

def set_binary_tensor(anomaly_score,t,data_shape):
  def set_index(num,data_shape):
    pass

  B1 = {}
  for i,row in enumerate(anomaly_score):
    idx = set_index(i,data_shape)
    if row[2] > t:
      #連番をインデックスに直す
      B1[idx] = 1
    else:
      B1[idx] = 0

  B1 = {}
  for indices in anomaly_score:
    if anomaly_score[indices] > t:
      B1[indices] = 1
    else:
      B1[indices] = 0

  return B1