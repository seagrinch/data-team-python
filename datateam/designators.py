""" OOI Datateam Import - Designator Functions """
import csv
import time
from .common import *


def find(db, table, reference_designator):
  """Find by reference_designator"""
  sql = 'reference_designator="%s"' % reference_designator
  result = db.select(table,sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db, table, data, columns):
  """Save an Instrument to the database"""
  data = remove_extraneous_columns(columns, data)

  id = find(db,table,data['reference_designator'])
  if id == False:
    data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert(table, data)
    print "Created: " +data['reference_designator']
  else:
    data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update(table, id, data)
    print "Updated: " +data['reference_designator']


def load_regions(db):
  """Load array Regions into the database"""
  columns = ['reference_designator', 'name', 'latitude', 'longitude']
  with open("infrastructure/regions.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      save(db, 'regions', row, columns)


def load_sites(db):
  """Load Sites into the database"""
  columns = ['reference_designator', 'region_rd', 'array_name', 'name', 'description', 'bottom_depth', 'longitude', 'latitude']
  with open("infrastructure/sites.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      row['region_rd'] = row['reference_designator'][:2]
      save(db, 'sites', row, columns)


def load_nodes(db):
  """Load Nodes into the database"""
  columns = ['reference_designator', 'region_rd', 'site_rd', 'name']
  with open("infrastructure/nodes.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      #row['region_rd'] = row['reference_designator'][:2]
      row['site_rd'] = row['reference_designator'][:8]
      save(db, 'nodes', row, columns)


def load_instruments(db):
  """Load Instruments into the database"""

  # Load in the Instrument Classes file for lookups
  catalogfile = 'infrastructure/instrument_classes.csv'
  vocab={}
  with open(catalogfile, 'rU') as csvfile: # was rb
    reader = csv.DictReader(csvfile)
    for row in reader:
      vocab[row['class']] = row['name']

  # Save the Instrument
  columns = ['reference_designator', 'region_rd', 'site_rd', 'node_rd', 'name', 'start_depth', 'end_depth', 'location']
  with open("infrastructure/instruments.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      #row['region_rd'] = row['reference_designator'][:2]
      #row['site_rd'] = row['reference_designator'][:8]
      row['node_rd'] = row['reference_designator'][:14]
      row['name'] = find_vocab(vocab, row['reference_designator'][18:23])
      save(db, 'instruments', row, columns)


def find_vocab(vocab, designator):
  """Vocabulary Lookup"""
  if designator in vocab.keys():
    return vocab[designator]
  else :
    return designator
