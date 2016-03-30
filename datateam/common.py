""" OOI Datateam Import Module - Common Functions """

def remove_extraneous_columns(headers, data_dict):
  """Get rid of extraneous columns"""
  
  # Remove items not in the header list
  unmatched = [x for x in data_dict.keys() if x not in set(headers)]
  [data_dict.pop(x) for x in unmatched]  
  
  # Remove items with blank values
  unmatched = [k for k,v in data_dict.items() if v =='']
  [data_dict.pop(x) for x in unmatched]  
  
  return data_dict