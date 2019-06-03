import pandas as pd

def get_id_num(uniq_list):
  id_dict = {}
  for i,v in enumerate(uniq_list):
    id_dict[v] = i+1
  return id_dict


df = pd.read_csv('/Users/kojimajun/MultiAspectSpotting/result_edit_anno_port003.csv')

ip_src = df['ip_src'].unique()
ip_src_id = get_id_num(ip_src)

ip_dst = df['ip_dst'].unique()
ip_dst_id = get_id_num(ip_dst)

dst_port = df['dst_port'].unique()
dst_port_id = get_id_num(dst_port)

df['ip_src_id'] = df['ip_src'].map(ip_src_id)
df['ip_dst_id'] = df['ip_dst'].map(ip_dst_id)
df['dst_port_id'] = df['dst_port'].map(dst_port_id)

df.to_csv('/Users/kojimajun/MultiAspectSpotting/result_edit_anno_id_port003.csv',
 columns=['ip_src_id','ip_dst_id','dst_port_id','epoch_time'],
 index=False,header=False)

df.to_csv('/Users/kojimajun/MultiAspectSpotting/result_edit_anno_all_port003.csv',
 index=False,header=True)