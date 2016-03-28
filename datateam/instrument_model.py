# OOI Datateam Instrument Model Functions
import csv
import time
from .common import *

def find(db,instrument_class, instrument_series):
  """Find an Instrument Model"""
  sql = 'class="%s" AND series="%s"' % (instrument_class,instrument_series)
  result = db.select('instrument_models',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db,data):
  """Save an Instrument Model to the database"""
  columns = ['class', 'series', 'manufacturer', 'model']
  data = remove_extraneous_columns(columns, data)

  id = find(db,data['class'], data['series'])
  if id == False:
    data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert('instrument_models', data)
    print "Created Instrument Model: " +data['class'] +'-' +data['series']
  else:
    data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('instrument_models', id, data)
    print "Updated Instrument Model: " +data['class'] +'-' +data['series']


def load(db):
  """Load Instrument Models into the database"""
  with open("instrument_models.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db,row)
