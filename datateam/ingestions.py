""" OOI Data Team Import Module - Ingestion Information """
import csv
# import time
from .common import *
# import openpyxl as xl
# import re
import glob


def find_ingestion(db,reference_designator,deployment,method):
  """Find an Ingestion"""
  sql = 'reference_designator="%s" AND deployment="%s" AND method="%s"' % (reference_designator, deployment, method)
  result = db.select('ingestions',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save_ingestion(db,data):
  """Save an Ingestion to the database"""
  id = find_ingestion(db,data['reference_designator'],data['deployment'],data['method'])
  if id == False:
    res = db.insert('ingestions', data)
    print "Created ingestion: " + data['reference_designator'] + ' ' + str(data['deployment']) + ' ' + data['method']
  else:
    res = db.update('ingestions', id, data)
    print "Updated ingestion: " + data['reference_designator'] + ' ' + str(data['deployment']) + ' ' + data['method']


def load(db):
  """Load Ingestions into the database"""
  r = db.truncate_table('ingestions')
  print "Truncated ingestions table"

  # Allowed columns
  columns = ['reference_designator','deployment','method','status','notes']

  # Read in Ingestion data
  file_mask = "repos/ingestion-csvs/*"
  directory_list = glob.glob(file_mask)
  for directory in directory_list:
    file_list = glob.glob(directory + '/*.csv')
    for ifile in file_list:
      with open(ifile, 'rb') as csvfile:
        print "Loading file: " + ifile
        reader = csv.DictReader(csvfile)
        for row in reader:
          if row['reference_designator']:
            row['method'] = row['data_source']
            row['deployment'] = ifile.split('/')[-1].split('_')[1][1:]
            data = remove_extraneous_columns(columns, row)
            save_ingestion(db,data)
