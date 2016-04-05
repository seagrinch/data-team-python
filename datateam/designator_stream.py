""" OOI Datateam Import Module - Designator-Stream Model Functions """
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
  """Load Designator/Stream linking table into the database"""
  r = db.truncate_table('designators_streams')
  print "Truncated table rows deleted " +str(r)

  with open("designators_streams.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      data={};
      data['designator_id'] = find(db,'designators','reference_designator',row['reference_designator'])
      data['stream_id'] = find(db,'streams','name',row['stream_name'])

      if (data['designator_id'] == False):
        print 'Not found: ' + row['reference_designator']
      if (data['stream_id'] == False):
        print 'Not found: ' + row['stream_name']
      if (data['designator_id'] and data['stream_id']):
        res = db.insert('designators_streams', data)
      

  print "Step 5 - Designator-Stream Joins Loaded"
