""" OOI Datateam Import Module - Asset Functions """
import csv
from datetime import datetime
from .common import *
import glob

def find(db,asset_uid):
  """Find an Asset by asset_uid"""
  sql = 'asset_uid="%s"' % asset_uid
  result = db.select('assets',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db,data):
  """Save an Asset to the database"""
  if data['ASSET_UID']:
    try:
      aqtime = datetime.strptime(data['ACQUISITION DATE'], '%Y%m%d').strftime('%Y-%m-%d')
    except:
      aqtime = ''
    
    newdata= {
      'asset_uid': data['ASSET_UID'],
      'type': data['TYPE'],
      'mobile': data['Mobile'],
      'description_of_equipment': data['DESCRIPTION OF EQUIPMENT'],
      'manufacturer': data['Manufacturer'],
      'model': data['Model'],      
      'manufacturer_serial_no': data["Manufacturer's Serial No./Other Identifier"],
      'firmware_version': data['Firmware Version'],
      'acquisition_date': aqtime,
      'original_cost': data['ORIGINAL COST'],
      'comments': data['comments'],
      }
  
    columns = ['asset_uid', 'type','mobile', 'description_of_equipment', 'manufacturer', 'model', 
      'manufacturer_serial_no', 'firmware_version', 'acquisition_date', 'original_cost', 'comments',
      ]
    data = remove_extraneous_columns(columns, newdata)
  
    id = find(db,data['asset_uid'])
    if id == False:
      res = db.insert('assets', data)
      print "Created Asset: " +data['asset_uid']
    else:
      res = db.update('assets', id, data)
      print "Updated Asset: " +data['asset_uid']
  else:
    print "No asset_uid, skipping row"


def load(db):
  """Load Assets into the database"""
  # Truncate table
  r = db.truncate_table('assets')
  print "Truncated assets table - Rows deleted: " +str(r)

  # Iterate over each Asset file
  file_mask = "repos/asset-management/bulk/*_bulk_load-AssetRecord.csv"
  file_list = glob.glob(file_mask)

  for ifile in file_list:
    with open(ifile, 'rb') as csvfile:
      print "Loading file: " + ifile
      reader = csv.DictReader(csvfile)
      for row in reader:
        save(db,row)
