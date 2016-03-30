""" OOI Datateam Import Module - Instrument Class Functions """
import csv
import time
from .common import *

def find(db,instrument_class):
  """Find an Instrument Class by class"""
  sql = 'class="%s"' % instrument_class
  result = db.select('instrument_classes',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db,data):
  """Save an Instrument Class to the database"""
  columns = ['class', 'name', 'description', 'primary_science_dicipline']
  data = remove_extraneous_columns(columns, data)

  id = find(db,data['class'])
  if id == False:
    data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert('instrument_classes', data)
    print "Created Instrument Class: " +data['class']
  else:
    data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('instrument_classes', id, data)
    print "Updated Instrument Class: " +data['class']


def load(db):
  """Load Instrument Classes into the database"""
  with open("instrument_classes.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db,row)
