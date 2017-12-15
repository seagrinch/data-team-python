#!/usr/bin/env python
# OOI Datateam Import - Script to Import Data Annotations

import datateam
import argparse
import datetime
import requests

# Command Line Arguments
parser = argparse.ArgumentParser(description='OOI Data Team Portal - Annotation Importer')
parser.add_argument('-s','--server',
  choices=['production','development'],
  default='development',
  help='Database server')
args = parser.parse_args()


def load_m2m_config():
  """Load M2M configuration"""
  import ConfigParser
  config = ConfigParser.ConfigParser()
  config.readfp(open('config.cfg'))
  return {
    'username': config.get('ooinet','username'),
    'password': config.get('ooinet','password')
  }   

# Allowed columns
columns = ['id','reference_designator','method','stream','parameter',
  'start_datetime','end_datetime','annotation',
  'exclusionFlag','qcFlag','source']

def save(db, data):
  """Save annotation to the database"""
  data = datateam.common.remove_extraneous_columns(columns, data)
  res = db.insert('annotations', data)
  print "Added: %s %s" % (data['reference_designator'], (data['start_datetime'] if 'start_datetime' in data else ''))


def create_url(start_id):
  url = ('https://ooinet.oceanobservatories.org/api/m2m/12580/anno?max_100&start_id={start_id}').format(start_id=start_id)
  return url


def convert_time(s):
  s = s/1000; #Convert from milliseconds 
  return datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S')


def process_row(row):
  #row['id'] = row['id']
  row['reference_designator'] = row['subsite'] 
  if (row['node']):
    row['reference_designator'] = "%s-%s" % (row['subsite'], row['node'])
  if (row['sensor']):
    row['reference_designator'] = "%s-%s-%s" % (row['subsite'], row['node'], row['sensor'])
  #row['method'] = row['method']
  #row['stream'] = row['stream']
  #row['parameter'] = row['parameter']
  if (row['beginDT']):
    row['start_datetime'] = convert_time(row['beginDT'])
  if (row['endDT']):
    row['end_datetime'] = convert_time(row['endDT'])
  #row['annotation'] = row['annotation'].decode('utf-8', errors='replace')
  #row['exclusionFlag'] = 1 if row['exclusionFlag']=='true' else 0
  #row['qcFlag'] = row['qcFlag']
  #row['source'] = row['source'] #if 'ReviewedBy' in row else ''
  return row


def load_annotations(db):
  """Load Annotations"""
  r = db.truncate_table('annotations')
  print "Truncated annotations table"

  # Load config information
  config = load_m2m_config()

  # Extract All Annoations
  result_length = 100
  start_id = 1
  while result_length ==100:
    url = create_url(start_id)
    # Grab Annotations data from API
    data = requests.get(url, auth=(config['username'],config['password'])).json()
    for row in data:
      row = process_row(row)
      save(db,row) # Save to database
    result_length = len(data)
    start_id = data[-1]['id'] + 1
    print 'Finished: %d Annotations, Next id is %d' % (result_length,start_id)


def main():
  """Main function for command line execution"""
  db = datateam.MysqlPython()
  db.load_config(args.server)
  db.open_connection()
  load_annotations(db)
  datateam.import_log.log(db,'annotations')
  db.close_connection()


# Run main function when in comand line mode        
if __name__ == '__main__':
  main()
