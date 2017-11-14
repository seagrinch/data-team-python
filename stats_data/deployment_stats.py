#!/usr/bin/env python
# OOI Data Team Portal
# Calculate Deployment Statistics
# Written by Sage 9/22/17

import pandas as pd
import numpy as np
from dateutil.relativedelta import relativedelta
from dateutil.parser import parse
from dateutil.tz import tzutc
from datetime import datetime
import requests
import math

startTime = datetime.now()

#-------------------------
# Load M2M configuration
import ConfigParser
config = ConfigParser.ConfigParser()
config.readfp(open('../config.cfg'))
config = {
    'username': config.get('ooinet','username'),
    'password': config.get('ooinet','password')
  }   

#-------------------------
def check_date(d):
  try:
    dd = parse(d)
  except:
    dd = datetime.now(tzutc())
  return dd

def day_count(d1, d2):
  '''Returns the number of unique days between two datetimes'''
  d1 = parse(d1)
  d2 = check_date(d2)
  d  = abs(d2 - d1)
  return math.ceil(d.days + float(d.seconds)/3600/24)

def uframe_url(row):
  '''Construct a uFrame data url'''
  site = row['reference_designator'][:8]
  node = row['reference_designator'][9:14]
  inst = row['reference_designator'][15:]
  if site.startswith('RS'):
    method = 'streamed'
  elif site in ['CE02SHBP','CE04OSBP']:
    method = 'streamed'
  else:
    method = 'telemetered'
  stream = row['preferred_stream']
  start_date = parse(row['start_date']).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
  end_date = check_date(row['stop_date']).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
  #parameter = str(int(row['preferred_parameter']))
  url = 'https://ooinet.oceanobservatories.org/api/m2m/12576/sensor/inv/'+site+'/'+node+'/'+inst+'/'+method+'/'+stream+'?beginDT='+start_date+'&endDT='+end_date+'&limit=1000&parameters=7' #+parameter
  return url

def data_count(row):
  # if row['reference_designator']=='CE01ISSM-MFD37-03-CTDBPC000':
#   if (row['current_status'] not in ['Engineering','Camera'] and np.isfinite(row['preferred_parameter'])):
  if ( row['current_status'] not in ['Engineering','Camera'] and len(str(row['preferred_stream']))>3 and row['reference_designator'][:2]=='CE'):
    url = uframe_url(row)
    print 'Retrieving ' + row.reference_designator + ' Deployment: ' + str(row.deployment_number)
    data = requests.get(url, auth=(config['username'],config['password']))
    if (data.status_code==200):
      try:
        uf = pd.read_json(data.text)
        uf['ymd'] = uf['time'].apply(lambda x: datetime(1900,1,1) + relativedelta(seconds = x))
        uf['ymd'] = uf['ymd'].apply(lambda x: x.strftime('%Y-%m-%d'))
        return uf['ymd'].unique().size
      except:
        print "  Failed parsing JSON for " + url
        return -2
    elif (data.status_code==500):
      print "  No data Returned"
      return 0
  else:
    print 'Skipping ' + row.reference_designator + ' Deployment: ' + str(row.deployment_number)
    return np.nan



#-------------------------
# First, load in master Deployment List
filename = 'deployments.csv'
print 'Loading: ' + filename 
deployments = pd.read_csv(filename)

# Calculate Deployment Days
deployments['deployment_days'] = deployments.apply(lambda row: day_count(row['start_date'],row['stop_date']), axis=1)

# Calculate Data Days
deployments['data_days'] = deployments.apply(lambda row: data_count(row), axis=1)

# Calculate percentage
deployments['percentage'] = deployments['data_days'] / deployments['deployment_days'] * 100


# Small Subset for testing
# deployments[deployments.reference_designator=='CE01ISSM-MFD37-03-CTDBPC000']


#-------------------------
# Output data file
deployments.to_csv('test_ce_1.csv',header=True)

print "Elapsed time: " + str(datetime.now() - startTime)

