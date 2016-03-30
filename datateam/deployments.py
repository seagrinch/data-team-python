# OOI Datateam - Deployments
import csv
import time
from .common import *
import openpyxl as xl
import re
import glob

def find(db,reference_designator,deployment_number):
  """Find an Deployment by reference_designator and deployment_number"""
  sql = 'reference_designator="%s" AND deployment_number="%s"' % (reference_designator, deployment_number)
  result = db.select('deployments',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db,data):
  """Save an Deployment to the database"""
  id = find(db,data['reference_designator'],data['deployment_number'])
  if id == False:
#     data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert('deployments', data)
    print "Created Deployment: " +data['reference_designator'] +' deployment #' +str(data['deployment_number'])
  else:
#     data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('deployments', id, data)
    print "Updated Deployment: " +data['reference_designator'] +' deployment #' +str(data['deployment_number'])


def load(db):
  """Load Assets into the database"""
  file_mask = "repos/asset-management/deployment/Omaha_Cal_*.xlsx"
  file_list = glob.glob(file_mask)
  
  # Problem files for testing
  #file_list = ['repos/asset-management/deployment/Omaha_Cal_Info_CP05MOAS-GL388_00002.xlsx'] # missing glider
  #file_list = ['repos/asset-management/deployment/Omaha_Cal_Info_CE01ISSP_00002.xlsx']# no inserts
  #file_list = ['repos/asset-management/deployment/Omaha_Cal_Info_RS03INT1.xlsx'] #time value have date and time
  #file_list = ['repos/asset-management/deployment/Omaha_Cal_Info_CP02PMUI_00004.xlsx'] #longitude truncated
  #file_list = ['repos/asset-management/deployment/Omaha_Cal_Info_CP05MOAS-GL376_00002.xlsx'] #wrong worksheet name
  #file_list = ['repos/asset-management/deployment/Omaha_Cal_Info_RS03CCAL.xlsx'] #refdes has an extra space
  #file_list = ['repos/asset-management/deployment/Omaha_Cal_Info_RS03INT1.xlsx'] #recover_date has time included
  
  for xlfile in file_list:
    print "Processing... " +xlfile
    wb = xl.load_workbook(filename=xlfile, read_only=True)
  
    if set(['Moorings']).issubset(wb.get_sheet_names()):
      m_data = crawl_worksheet(wb['Moorings'])
      moor_header = [str(x).lower().replace(" ", "_") for x in m_data[0]]
  
      # Iterate through 'Moorings' sheet data matrix
      for row in m_data[1:]:  # Skip the first row, because all cal sheets have headers
        if row == [None] * len(row):  # Check for empty rows and skip
          continue
        else:  # Go through the data and upload to the database
          moor_dict = dict(zip(moor_header, row))  # Zip the headers and data rows into a dictionary
          if moor_dict['ref_des'] and moor_dict['deployment_number']:
            moor_dict = clean_mooring_data(moor_dict)  # Create valid data types for mysql db
            #print moor_dict
            save(db,moor_dict)
  

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


def clean_mooring_data(data_dict):
    """Clean deployment table items and rename some column"""
    
    data_dict['reference_designator'] = data_dict['ref_des'].strip() # Remove extra spaces
    data_dict['mooring_barcode'] = data_dict['mooring_ooibarcode']
    data_dict['mooring_serial_number'] = data_dict['serial_number']

    m_h = ['reference_designator', 'mooring_barcode', 'mooring_serial_number', 'deployment_number', 
           'anchor_launch_date', 'anchor_launch_time', 'recover_date', 'latitude', 'longitude', 
           'water_depth', 'cruise_number', 'notes']
    data_dict = remove_extraneous_columns(m_h, data_dict)

    if data_dict['anchor_launch_date'] is not None:
        #data_dict['anchor_launch_date'] = re.sub("[^0123456789:-]", " ", str(data_dict['anchor_launch_date']))
        a = re.search(r"(\d+)-(\d+)-(\d+)", str(data_dict['anchor_launch_date']))
        if a:
          data_dict['anchor_launch_date'] = a.group(0)
        else:
        #if data_dict['anchor_launch_date'].strip() == '':
          data_dict.pop('anchor_launch_date')

    if data_dict['anchor_launch_time'] is not None:
        a = re.search(r'(\d+):(\d+)(:(\d+))?', str(data_dict['anchor_launch_time']))
        if a:
          data_dict['anchor_launch_time'] = a.group(0)
        else:
          data_dict.pop('anchor_launch_time')

    if data_dict['recover_date'] is not None:
        a = re.search(r"(\d+)-(\d+)-(\d+)", str(data_dict['recover_date']))
        if a:
          data_dict['recover_date'] = a.group(0)
        else:
          data_dict.pop('recover_date')
            
    if data_dict['latitude'] is not None:
        if isinstance(data_dict['latitude'], unicode):
            try:
                data_dict['latitude'] = str(data_dict['latitude'])
            except UnicodeEncodeError:
                data_dict["latitude"] = conversion(data_dict["latitude"])
        elif isinstance(data_dict['latitude'], float):
            data_dict['latitude'] = str(data_dict['latitude'])
        try:
          float(data_dict['latitude'])
        except ValueError:
          data_dict.pop('latitude')

    if data_dict['longitude'] is not None:
        if isinstance(data_dict['longitude'], unicode):
            try:
                data_dict['longitude'] = str(data_dict['longitude'])
            except UnicodeEncodeError:
                data_dict["longitude"] = conversion(data_dict["longitude"])
        elif isinstance(data_dict['longitude'], float):
            data_dict['longitude'] = str(data_dict['longitude'])
        try:
          float(data_dict['longitude'])
        except ValueError:
          data_dict.pop('longitude')

    if data_dict['water_depth'] is not None:
        data_dict['water_depth'] = re.sub("[^0123456789]", "", str(data_dict['water_depth']))
        if data_dict['water_depth'].strip() == '':
          data_dict.pop('water_depth')

    return data_dict


# def remove_extraneous_columns(headers, data_dict):
#     unmatched = [x for x in data_dict.keys() if x not in set(headers)]
#     [data_dict.pop(x) for x in unmatched]  # get rid of extraneous columns
#     return data_dict
