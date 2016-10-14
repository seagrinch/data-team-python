""" OOI Datateam Import Module - Cruise Import Functions """
import csv
from datetime import datetime
from .common import *

def find(db,cuid):
  """Find an Asset by cuid"""
  sql = 'cuid="%s"' % cuid
  result = db.select('cruises',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db,data):
  """Save a Cruise to the database"""
  if data['CUID']:
    newdata= {
      'cuid': data['CUID'],
      'ship_name': data['ShipName'],
      'cruise_start_date': data['cruiseStartDateTime'],
      'cruise_end_date': data['cruiseStopDateTime'],
      'notes': data['notes'],
      }
  
    columns = ['cuid', 'ship_name','cruise_start_date', 'cruise_end_date', 'notes']
    data = remove_extraneous_columns(columns, newdata)
  
    id = find(db,data['cuid'])
    if id == False:
      res = db.insert('cruises', data)
      print "Created Cruise: " +data['cuid']
    else:
      res = db.update('cruises', id, data)
      print "Updated Cruise: " +data['cuid']
  else:
    print "No cuid, skipping row"


def load(db):
  """Load Cruises into the database"""
  # Truncate table
  r = db.truncate_table('cruises')
  print "Truncated cruises table - Rows deleted: " +str(r)

  with open("repos/asset-management/cruise/CruiseInformation.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db,row)
