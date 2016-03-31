""" OOI Datateam Import - Designator Functions """
import csv
import time
from .common import *


def find(db,reference_designator):
  """Find by reference_designator"""
  sql = 'reference_designator="%s"' % reference_designator
  result = db.select('designators',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db,data,columns,designator_type, parent):
  """Save an Instrument to the database"""
  data = remove_extraneous_columns(columns, data)
  data['designator_type'] = designator_type
  data['parent_designator'] = parent

  id = find(db,data['reference_designator'])
  if id == False:
    data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert('designators', data)
    print "Created: " +data['reference_designator']
  else:
    data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('designators', id, data)
    print "Updated: " +data['reference_designator']


def load_sites(db):
  """Load sites into the database"""
  columns = ['reference_designator', 'name', 'latitude', 'longitude']
  with open("sites.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db, row, columns, 'site', '')


def load_platforms(db):
  """Load platforms into the database"""
  columns = ['reference_designator', 'name', 'description', 'end_depth', 'latitude', 'longitude']
  with open("platforms.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db, row, columns, 'platform', row['reference_designator'][:2])


def load_nodes(db):
  """Load nodes into the database"""
  columns = ['reference_designator', 'name', 'description', 'latitude', 'longitude', 'bottom_depth']
  with open("nodes.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db, row, columns, 'node', row['reference_designator'][:8])


def load_instruments(db):
  """Load instruments into the database"""

  # Load in the Instrument Classes file for lookups
  catalogfile = 'instrument_classes.csv'
  vocab={}
  with open(catalogfile, 'rU') as csvfile: # was rb
    reader = csv.DictReader(csvfile)
    for row in reader:
      vocab[row['class']] = row['name']

  # Save the Instrument
  columns = ['reference_designator', 'name', 'type', 'description', 'start_depth', 'end_depth', 'location']
  with open("instruments.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      row['name'] = find_vocab(vocab, row['reference_designator'][18:23])
      save(db, row, columns, 'instrument', row['reference_designator'][:14])


def find_vocab(vocab, designator):
  """Vocabulary Lookup"""
  if designator in vocab.keys():
    return vocab[designator]
  else :
    return designator
