""" OOI Datateam Import Module - Data Stream Model Functions """
#import sqlite3
import csv
import time
#from .common import *

def find(db,table,column_name,id):
  """Find an id in a table"""
  sql = '%s="%s"' % (column_name,id)
  result = db.select(table,sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def load(db):
  """Load Data Streams into the database"""
  r = db.truncate_table('data_streams')
  print "Truncated data_streams table - Rows deleted: " +str(r)

  with open("infrastructure/data_streams.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      row['instrument_id'] = find(db,'instruments','reference_designator',row['reference_designator'])
      row['stream_id'] = find(db,'streams','name',row['stream_name'])

      if (row['instrument_id'] == False):
        print 'Instrument Not found: ' + row['reference_designator']
      if (row['stream_id'] == False and row['stream_name']):
        print 'Stream Not found: ' + row['stream_name']
      if (row['instrument_id'] and row['stream_id']):
        res = db.insert('data_streams', row)
        print "Loaded: " +row['reference_designator'] +' ' +row['stream_name'] +' ' +row['method']
  print "Data Streams Loaded"
