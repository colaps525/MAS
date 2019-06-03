

def set_binary_tensor(anomaly_score,t):
  B1 = {}
  for indices in anomaly_score:
    if anomaly_score[indices] > t:
      B1[indices] = 1
    else:
      B1[indices] = 0

  return B1