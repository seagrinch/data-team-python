#!/usr/bin/env python
# OOI Data Team Portal
# Calculate Quarterly uFrame Data Statistics by Instrument
# Written by Sage 6/22/17

import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime
import requests
import time

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
# Load in Operational Status
xlfile = 'ExpectedData_20170621.xlsx'
print 'Loading: ' + xlfile 
df_ops = pd.read_excel(xlfile, sheetname='refdes2.csv')

# Extract list of months and unique instruemnts
months = df_ops.columns[4:]
instruments = df_ops['reference_designator'].unique()

# Create empty output arrays
output_ts  = pd.DataFrame(columns=months)
output_rec = pd.DataFrame(columns=months)

# Add reference columns
output_ts['reference_designator'] = instruments
output_ts['site'] = output_ts['reference_designator'].str.slice(0,8)
output_ts['array'] = output_ts['reference_designator'].str.slice(0,2)
output_rec['reference_designator'] = instruments
output_rec['site'] = output_rec['reference_designator'].str.slice(0,8)
output_rec['array'] = output_rec['reference_designator'].str.slice(0,2)

#-------------------------
# Process statistics for each Instrument and Month
for index,row in output_ts.iterrows(): 
  time.sleep(1)
  print "Processing: " + str(index) + ' ' + row['reference_designator']
  
  site = row['reference_designator'][:8]
  node = row['reference_designator'][9:14]
  inst = row['reference_designator'][15:]
  url = 'https://ooinet.oceanobservatories.org/api/m2m/12576/sensor/inv/'+site+'/'+node+'/'+inst+'/metadata/times?partition=true'

  # Grab Cassandra data from API
  data = requests.get(url, auth=(config['username'],config['password']))  
  if data.status_code == 200:
    df = pd.read_json(data.text)
    if df.size > 0:
      df = df[df['count']>1] # Remove rows with only 1 count
      df['beginTime'] = pd.to_datetime(df['beginTime'], errors='coerce') # Convert timestamps
      df['endTime'] = pd.to_datetime(df['endTime'], errors='coerce')
  
      for month in months:
        stat_op = df_ops.loc[ (df_ops[month].isin(['Operational','Pending'])) & (df_ops['reference_designator']==row['reference_designator']) ]
        stat_ts = df.loc[ 
          (df['beginTime'] <= month + relativedelta(months=+1)) & 
          (df['endTime'] >= month) & 
          (df['method'].isin(['telemetered', 'streamed']))
        ]
        stat_rec = df.loc[ 
          (df['beginTime'] <= month + relativedelta(months=+1)) & 
          (df['endTime'] >= month) & 
          (df['method'].isin(['recovered', 'recovered_cspp', 'recovered_host', 'recovered_inst', 'recovered_wfp']))
        ]
        
        if (len(stat_op)>0 and len(stat_ts)>0):
          value_ts = 2 # All good
        elif len(stat_op) > 0:
          value_ts = 1 # Expected but not found in system
        elif len(stat_ts) > 0:
          value_ts = 3 # Found in system, but not expected
        else:
          value_ts = 0 # No date found or expected
          
        if (len(stat_op)>0 and len(stat_rec)>0):
          value_rec = 2 # All good
        elif len(stat_op) > 0:
          value_rec = 1 # Expected but not found in system
        elif len(stat_rec) > 0:
          value_rec = 3 # Found in system, but not expected
        else:
          value_rec = 0 # No date found or expected
  
        output_ts = output_ts.set_value(index,month,value_ts) 
        output_rec = output_rec.set_value(index,month,value_rec) 

#-------------------------
# Output data file
#output.to_csv('quarterly_instrument_output.csv',header=True)
writer = pd.ExcelWriter('quarterly_instrument_output.xlsx')
output_ts.to_excel(writer,'Telemetered Streamed')
output_rec.to_excel(writer,'Recovered')
writer.save()

print "Elapsed time: " + str(datetime.now() - startTime)
