# OOI Datateam Instrument Functions
import csv
import time
from .common import *

def find(db,reference_designator):
  """Find an Instrument by reference_designator"""
  sql = 'reference_designator="%s"' % reference_designator
  result = db.select('instruments',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db,data):
  """Save an Instrument to the database"""
  columns = ['reference_designator', 'name', 'type', 'description', 'start_depth', 'end_depth', 'location']
  data = remove_extraneous_columns(columns, data)

  id = find(db,data['reference_designator'])
  if id == False:
    data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert('instruments', data)
    print "Created Instrument: " +data['reference_designator']
  else:
    data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('instruments', id, data)
    print "Updated Instrument: " +data['reference_designator']


def load(db):
  """Load Instruments into the database"""
  with open("instruments.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db,row)
