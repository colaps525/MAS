import pandas as pd

def attr_to_id(path):
  def get_id_num(uniq_list):
    id_dict = {}
    for i,v in enumerate(uniq_list):
      id_dict[v] = i
    return id_dict

  df = pd.read_csv(path)
  cols = list(df.columns)
  #最後の１列は値とする
  value_col = cols[-1]
  cols.pop()

  col_name_orig = []
  dim_cols = []
  for col in cols:
    col_attr = df[col].unique()
    col_id = get_id_num(col_attr)
    col_name = str(col) + '_for_cp_calc_id'
    col_name_orig.append(col)
    dim_cols.append(col_name)
    df[col_name] = df[col].map(col_id)
    df.astype({col_name:'int64'})

  target_cols = dim_cols[:]
  target_cols.append(value_col)
  df.astype({value_col:'float64'})
  df_id = df[target_cols]
  df_id.to_csv('/Users/kojimajun/MultiAspectSpotting/result_edit_anno_id_for_python_port003.csv',index=False,header=False)

  #df.to_csv('/Users/kojimajun/MultiAspectForensics/Python/MAF/result_all.csv',index=False,header=True)

  return df,dim_cols,value_col,col_name_orig


if __name__ == '__main__':
  path = '/Users/kojimajun/MultiAspectSpotting/result_edit_anno_port003.csv'
  attr_to_id(path)