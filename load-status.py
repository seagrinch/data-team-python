#!/usr/bin/env python
# OOI Data Team Portal
# Tool to check and load operational status

import datateam
import argparse
import csv
import requests
from datetime import datetime, timedelta

# Command Line Arguments
parser = argparse.ArgumentParser(description='OOI Data Team Portal - Operational Status')
parser.add_argument('-s','--server',
  choices=['production','development'],
  default='development',
  help='Database server to use')
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


def load_instrument_list():
  """Load instruments list from CSV file"""
  with open("infrastructure/instruments.csv", 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    instruments=[]
    for row in reader:
      instruments.append(row)
    return instruments


def create_url(reference_designator,stream):
  """Create uFrame M2M url for last 24 hours"""
  site = reference_designator[:8]
  node = reference_designator[9:14]
  inst = reference_designator[15:]
  if site[0:2] == 'RS':
    delivery_method = 'streamed'
  elif site in ['CE02SHBP','CE04OSBP']:
    delivery_method = 'streamed'
  else:
    delivery_method = 'telemetered'
  end_date = datetime.utcnow()
  start_date = end_date - timedelta(1)
  url = ('https://ooinet.oceanobservatories.org/api/m2m/12576/sensor/inv/{site}/{node}/{inst}'
         '/{delivery_method}/{stream}?beginDT={start_time}&endDT={end_time}&limit=1000&parameters=7').format(
           site=site, node=node, inst=inst,
           delivery_method=delivery_method, stream=stream,
           start_time = start_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'), 
           end_time = end_date.strftime('%Y-%m-%dT%H:%M:%S.000Z'))
  return url


def save_csv(data):
  """Save status data to CSV file"""
  filename = 'instrument_status_%s.csv' % datetime.now().strftime('%Y%m%d')
  with open(filename, 'w') as csvfile:
    fieldnames = ['reference_designator', 'current_status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in data:
      writer.writerow({'reference_designator': row['reference_designator'], 'current_status': row.get('current_status')})


def load_instrument_status(db):
  """Load instruments, check status, and update database"""
  # Load config information
  config = load_m2m_config()
  # Load Instrument List
  instruments = load_instrument_list()
  # Loop over each instrument
  for row in instruments:
    if not row['current_status'] and row['preferred_stream']:
      print 'Checking ' + row['reference_designator']
      url = create_url(row['reference_designator'],row['preferred_stream'])
      # Grab Cassandra data from API
      data = requests.get(url, auth=(config['username'],config['password']))
      # Check current status
      if data.status_code == 200 and len(data.json())>2:
        row['current_status'] = 'Operational'
      else:
        row['current_status'] = 'Not Operational'
      # Save to database
      print "  Code: %d Length: %d Status: %s" % ( data.status_code, len(data.json()), row['current_status'] )
      datateam.designators.save(db, 'instruments', row, ['reference_designator', 'current_status'])

    else:
      print 'Skipping: ' + row['reference_designator']
  
  # Save to CSV
  save_csv(instruments)


def main():
  """Main function for command line execution"""
  db = datateam.MysqlPython()
  db.load_config(args.server)
  db.open_connection()
  load_instrument_status(db)  
  datateam.import_log.log(db,'status_check')
  db.close_connection()


# Run main function when in comand line mode        
if __name__ == '__main__':
  main()
