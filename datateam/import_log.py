""" OOI Data Team Import Module - Import Log Functions """
import time
from .common import *

# Allowed columns
columns = ['name','import_date','comment','created','modified']


def find(db,name):
  """Find an Import Log by name"""
  sql = 'name="%s"' % name
  result = db.select('import_log',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False

def save(db,data):
  """Save an Import Log to the database"""
  data = remove_extraneous_columns(columns, data)

  id = find(db,data['name'])
  if id == False:
    data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert('import_log', data)
    print "Created Import Log: " +data['name']
  else:
    data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('import_log', id, data)
    print "Updated Import Log: " +data['name'] 

def log(db,name):
  data = {
    'name':name,
    'import_date':time.strftime('%Y-%m-%d %H:%M:%S')
  }
  save(db,data)
