# OOI Datateam Platform Functions
import csv
import time
from .common import *

def find(db,reference_designator):
  """Find a Platform by reference_designator"""
  sql = 'reference_designator="%s"' % reference_designator
  result = db.select('platforms',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db,data):
  """Save a Platform to the database"""
  columns = ['reference_designator', 'name', 'description', 'bottom_depth', 'latitude', 'longitude']
  data = remove_extraneous_columns(columns, data)

  id = find(db,data['reference_designator'])
  if id == False:
    data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert('platforms', data)
    print "Created Platform: " +data['reference_designator']
  else:
    data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('platforms', id, data)
    print "Updated Platform: " +data['reference_designator']


def load(db):
  """Load Platforms into the database"""
  with open("platforms.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db,row)
