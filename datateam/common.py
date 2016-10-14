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

def conversion(old):
    """
    Convert degrees minutes seconds to decimal degrees
    :param old: degrees minutes seconds
    :return: decimal degrees
    """
    # old = str(old)
    direction = {'N': 1, 'S': -1, 'E': 1, 'W': -1}
    new = old.replace(u'\xb0', ' ').replace('\'', ' ').replace('"', ' ')
    new = new.split()
    new_dir = new.pop()
    new.extend([0, 0, 0])
    new[0] = re.sub("[^0123456789.]", "", new[0])
    new[1] = re.sub("[^0123456789.]", "", new[1])
    return (int(new[0])+float(new[1])/60.0) * direction[new_dir]


def crawl_worksheet(ws):
    """
    Crawl through worksheet and grab data
    :param ws: the open worksheet
    :return: return the data in a matrixy
    """
    matrix = []
    for row in ws:
        row_m = []
        for col in row:
            try:
                row_m.append(col.value)
            except AttributeError:
                break
        matrix.append(row_m)
    return matrix
