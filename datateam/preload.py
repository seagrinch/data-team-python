""" OOI Datateam Import Module - Preload Model Functions """
import sqlite3
import csv
import time
#from .common import *

def find(db,table,id):
  """Find an id in a table"""
  sql = 'id="%s"' % (id)
  result = db.select(table,sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db, table, data):
  """Save a record to the database"""
  #columns = ['name','display_name','standard_name','parameter_precision','data_product_identifier','description']
  #data = remove_extraneous_columns(columns, data)

  id = find(db,table, data['id'])
  if id == False:
    #data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert(table, data)
    print "Created: " +table +str(data['id'])
  else:
    #data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update(table, id, data)
    print "Updated: " +table +str(data['id'])


def load(db):
  load_parameters(db)
  load_parameter_functions(db)
  load_streams(db)
  load_parameters_streams(db)


def load_parameters(db):
  """Load Parameters into the database"""
  conn = sqlite3.connect('repos/preload-database/preload.db')
  conn.row_factory = sqlite3.Row
  c = conn.cursor()

  # Load fill_values
  c.execute("SELECT * FROM fill_value")
  a = c.fetchall()
  fill_values={}
  for row in a:
    fill_values[row['id']] = row['value']

  # Load units
  c.execute("SELECT * FROM unit")
  a = c.fetchall()
  units={}
  for row in a:
    units[row['id']] = row['value']

  # Load parameters
  c.execute("SELECT * FROM parameter")
  a = c.fetchall()
  for row in a:
    data={};
    data['id'] = row['id']
    data['name'] = row['name']
    if (row['unit_id']):
      data['unit'] = units[row['unit_id']]
    if (row['fill_value_id']):
      data['fill_value'] = fill_values[row['fill_value_id']]
    data['display_name'] = row['display_name']
    data['standard_name'] = row['standard_name']
    data['parameter_precision'] = row['precision']
    data['parameter_function_id'] = row['parameter_function_id']
    data['parameter_function_map'] = row['parameter_function_map']
    data['data_product_identifier'] = row['data_product_identifier']
    data['description'] = row['description']
    
    save(db,'parameters',data)
    
  print "Step 1 - Parameters Loaded"


def load_parameter_functions(db):
  """Load Parameter Functions into the database"""
  conn = sqlite3.connect('repos/preload-database/preload.db')
  conn.row_factory = sqlite3.Row
  c = conn.cursor()

  # Load function_types
  c.execute("SELECT * FROM function_type")
  a = c.fetchall()
  function_types={}
  for row in a:
    function_types[row['id']] = row['value']

  # Load parameter_functions
  c.execute("SELECT * FROM parameter_function")
  a = c.fetchall()
  for row in a:
    data={};
    data['id'] = row['id']
    data['name'] = row['name']
    if (row['function_type_id']):
      data['function_type'] = function_types[row['function_type_id']]
    data['function'] = row['function']
    data['owner'] = row['owner']
    data['description'] = row['description']
    data['qc_flag'] = row['qc_flag']
    
    save(db,'parameter_functions',data)

  print "Step 2 - Parameter Functions Loaded"


def load_streams(db):
  """Load Streams into the database"""
  conn = sqlite3.connect('repos/preload-database/preload.db')
  conn.row_factory = sqlite3.Row
  c = conn.cursor()

  # Load streams
  c.execute("SELECT * FROM stream")
  a = c.fetchall()
  for row in a:
    data={};
    data['id'] = row['id']
    data['name'] = row['name']
    data['time_parameter'] = row['time_parameter']
    data['uses_ctd'] = row['uses_ctd']
    data['binsize_minutes'] = row['binsize_minutes']
    
    save(db,'streams',data)

  # Manual additions
  extras = [
    {'id':'9901','name':'camds_video'},
    {'id':'9902','name':'iris'},
    {'id':'9903','name':'ppsdn_status'},
    {'id':'9904','name':'rasfl_status'},
  ]
  for row in extras:
    save(db,'streams',row)
    
  print "Step 3 - Streams Loaded"

    
def load_parameters_streams(db):
  """Load Parameter/Stream linking table into the database"""
  # Truncate join table
  r = db.truncate_table('parameters_streams')
  print "Truncated table - Rows deleted: " +str(r)

  conn = sqlite3.connect('repos/preload-database/preload.db')
  conn.row_factory = sqlite3.Row
  c = conn.cursor()

  # Load streams
  c.execute("SELECT * FROM stream_parameter")
  a = c.fetchall()
  for row in a:
    data={};
    data['stream_id'] = row['stream_id']
    data['parameter_id'] = row['parameter_id']
    res = db.insert('parameters_streams', data)
    #print "Saved: " +str(data['stream_id']) + '-' +str(data['parameter_id'])
    
  print "Step 4 - Parameter-Stream Joins Loaded"
