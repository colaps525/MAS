from scapy.all import *
import collections
import pandas as pd
from datetime import datetime
import csv

file_list = [
#'/Users/kojimajun/MultiAspectForensics/lbl-internal.20041004-1313.port003.dump.anon-scanners'
'/Users/kojimajun/MultiAspectSpotting/lbl-internal.20041215-0209.port002.dump.anon'
]
result = {}

for path in file_list:
  with PcapReader(path) as packets:
    i = 0
    for p in packets:

      try:
        ip_src = p['IP'].src
      except:
        ip_src = 'NULL'

      try:
        ip_dst = p['IP'].dst
      except:
        ip_dst = 'NULL'

      try:
        dst_port = p['TCP'].dport
      except:
        dst_port = 'NULL'

      if ip_src != 'NULL' and ip_dst != 'NULL' and dst_port != 'NULL':

        packet_data = (ip_src,ip_dst,dst_port)

        if packet_data not in result.keys():
          result[packet_data] = 1
        else:
          result[packet_data] = result[packet_data] + 1
      i = i + 1
      if i % 10000 ==0:
        print(i)

df_key = pd.Series(list(result.keys()))
df_value = pd.Series(list(result.values()))

df = pd.concat([df_key, df_value],axis=1)

df.to_csv('/Users/kojimajun/MultiAspectSpotting/result_port002.csv',header=False,index=False)

