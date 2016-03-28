# OOI Datateam Node Functions
import csv
import time
from .common import *

def find(db,reference_designator):
  """Find a Node by reference_designator"""
  sql = 'reference_designator="%s"' % reference_designator
  result = db.select('nodes',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db,data):
  """Save a Node to the database"""
  columns = ['reference_designator', 'name', 'description', 'latitude', 'longitude', 'bottom_depth']
  data = remove_extraneous_columns(columns, data)

  id = find(db,data['reference_designator'])
  if id == False:
    data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert('nodes', data)
    print "Created Node: " +data['reference_designator']
  else:
    data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('nodes', id, data)
    print "Updated Node: " +data['reference_designator']


def load(db):
  """Load Nodes into the database"""
  with open("nodes.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db,row)
