# OOI Datateam Site Functions
import csv
import time
from .common import *

def find(db,reference_designator):
  """Find a Site by reference_designator"""
  sql = 'reference_designator="%s"' % reference_designator
  result = db.select('sites',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False
  
      
def save(db,data):
  """Save a Site to the database"""
  columns = ['reference_designator', 'name', 'latitude', 'longitude']
  data = remove_extraneous_columns(columns, data)
  
  id = find(db,data['reference_designator'])
  if id == False:
    data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert('sites', data)
    print "Created Site: " +data['reference_designator']
  else:
    data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('sites', id, data)
    print "Updated Site: " +data['reference_designator']


def load(db):
  """Load Sites into the database"""
  with open("sites.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db,row)



