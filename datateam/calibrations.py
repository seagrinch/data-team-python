""" OOI Data Team Import Module - Calibration Functions """
import csv
import time
from .common import *
import openpyxl as xl
import re
import glob


def find_cal(db,asset_uid,start_date,name):
  """Find a calibration"""
  sql = 'asset_uid="%s" AND start_date="%s" AND name="%s"' % (asset_uid, start_date, name)
  result = db.select('calibrations',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save_cal(db,data):
  """Save a calibration to the database"""
  id = find_cal(db,data['asset_uid'],data['start_date'],data['name'])
  if id == False:
    res = db.insert('calibrations', data)
    print "Created calibration: " +data['asset_uid'] +' Start Date: ' +str(data['start_date']) +' ' +data['name']
  else:
    #data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('calibrations', id, data)
    print "Updated calibration: " +data['asset_uid'] +' Start Date: ' +str(data['start_date']) +' ' +data['name']


def load(db):
  """Load calibrations into the database"""
  r = db.truncate_table('calibrations')
  print "Truncated calibrations table"

  # Allowed columns
  columns = ['class','asset_uid','start_date','serial','name','value','notes']

  # Read in calibration data
  file_mask = "repos/asset-management/calibration/*"
  directory_list = glob.glob(file_mask)
  for directory in directory_list:
    file_list = glob.glob(directory + '/*.csv')
    for ifile in file_list:
      with open(ifile, 'rb') as csvfile:
        print "Loading file: " + ifile
        reader = csv.DictReader(csvfile)
        for row in reader:
          row['class'] = directory.split('/')[-1]
          row['asset_uid'] = ifile.split('/')[-1].split('__')[0]
          row['start_date'] = ifile.split('/')[-1].split('__')[1].split('.')[0]
          data = remove_extraneous_columns(columns, row)
          save_cal(db,data)

