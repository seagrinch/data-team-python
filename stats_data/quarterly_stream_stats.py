#!/usr/bin/env python
# OOI Data Team Portal
# Calculate Quarterly uFrame Data Statistics
# Written by Sage 6/19/17

import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime
import requests

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
# First, load in master Instrument Streams list
filename = 'InstrumentStreams_20170619.csv'
print 'Loading: ' + filename 
df_master = pd.read_csv(filename)

#-------------------------
# Second, load in Operational Status
xlfile = 'ExpectedData_20170621.xlsx'
print 'Loading: ' + xlfile 
df_ops = pd.read_excel(xlfile, sheetname='refdes2.csv')

# Pull list of months from Ops Status
months = df_ops.columns[4:]

# Create output array
output = pd.concat([df_master,pd.DataFrame(columns=months)])

#-------------------------
# Process statistics for each Stream and Month
last_url = ''
for index,row in output.iterrows():  
  print "Processing: " + str(index) + ' ' + row['reference_designator'] + ' ' + row['method'] + ' ' + row['stream_name']
  
  site = row['reference_designator'][:8]
  node = row['reference_designator'][9:14]
  inst = row['reference_designator'][15:]
  url = 'https://ooinet.oceanobservatories.org/api/m2m/12576/sensor/inv/'+site+'/'+node+'/'+inst+'/metadata/times?partition=true'

  # Grab Cassandra data from API
  if url != last_url:
    print "  Getting new data"
    data = requests.get(url, auth=(config['username'],config['password']))  
    last_url = url
  if data.status_code == 200:
    df = pd.read_json(data.text)
    df = df[df['count']>1] # Remove rows with only 1 count
    df['beginTime'] = pd.to_datetime(df['beginTime'], errors='coerce')
    df['endTime'] = pd.to_datetime(df['endTime'], errors='coerce')

    for month in months:
      cc = df_ops.loc[ (df_ops[month].isin(['Operational','Pending'])) & (df_ops['reference_designator']==row['reference_designator']) ]
      dd = df.loc[ 
        (df['beginTime'] <= month + relativedelta(months=+1)) & 
        (df['endTime'] >= month) & 
        (df['method']==row['method']) & 
        (df['stream']==row['stream_name'])
      ]
      if (len(cc)>0 and len(dd)>0):
        output = output.set_value(index,month,2) # All good
      elif len(cc) > 0:
        output = output.set_value(index,month,1) # Expected but not found in system
      elif len(dd) > 0:
        output = output.set_value(index,month,3) # Found in system, but not expected
      else:
        output = output.set_value(index,month,0) # No date found or expected

#-------------------------
# Output data file
output.to_csv('quarterly_output.csv',header=True)

print "Elapsed time: " + str(datetime.now() - startTime)



