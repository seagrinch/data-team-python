#!/usr/bin/env python
# OOI Data Team Portal
# Calculate uFrame Data Statistics
# Written by Sage 3/29/17

import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime

startTime = datetime.now()

#-------------------------
# First, load in Operational Status

xlfile = 'ExpectedData_20170328.xlsx'
print 'Loading: ' + xlfile 
df_op = pd.read_excel(xlfile, sheetname='refdes2.csv')

sites = df_op['site'].unique()
months = df_op.columns[4:]

# Setup output arryas
output_ops = pd.DataFrame(index=sites,columns=months)
output_telemetered = pd.DataFrame(index=sites,columns=months)
output_recovered = pd.DataFrame(index=sites,columns=months)
output_streamed = pd.DataFrame(index=sites,columns=months)


#-------------------------
# Next, load in Cassandra Status
filename = 'partition_metadata_20170328.json'

# Read in Cassandra data csv as dataframe
print 'Loading: ' + filename 
df = pd.read_json(filename)

# Select only the columns we need
df = df[['referenceDesignator','method','stream','first','last','count']]

# Remove rows with only 1 count
df = df[df['count']>1]

# Convert Time
time_units = 'seconds since 1900-01-01'
df = df[(df['first'] < 1e+10) & (df['first'] > 1e+8)] # Hacks to deal with bad times
df = df[(df['last'] < 1e+10) & (df['last'] > 1e+8)] # Hacks to deal with bad times
df['first']= pd.to_timedelta(df['first'], unit='s') + pd.to_datetime('1900/1/1') #old way
df['last']= pd.to_timedelta(df['last'], unit='s') + pd.to_datetime('1900/1/1') #old way

# Merge recovered records
df.loc[df['method'].isin(['recovered', 'recovered_cspp', 'recovered_host', 'recovered_inst', 'recovered_wfp']),'method'] = 'recovered'

# Remove non-instruments
df = df[df['referenceDesignator'].str.len()==27]

# Add Site column
df['site'] = df['referenceDesignator'].str.slice(0,8)


#-------------------------
# Process statistics for each Site by month
for x in sites:
  print "Processing: " + x
  for y in months:
    cc = df_op.loc[ (df_op[y].isin(['Operational','Pending'])) & (df_op['site']==x) ]
    output_ops = output_ops.set_value(x,y,len(cc))
    
    dd = df.loc[ (df['first'] < y+relativedelta(months=+1)) & (df['last'] > y) & (df['site']==x) & (df['method']=='telemetered')]
    rd = dd['referenceDesignator'].unique()
    output_telemetered = output_telemetered.set_value(x,y,len(rd))
    
    dd = df.loc[ (df['first'] < y+relativedelta(months=+1)) & (df['last'] > y) & (df['site']==x) & (df['method']=='recovered')]
    rd = dd['referenceDesignator'].unique()
    output_recovered = output_recovered.set_value(x,y,len(rd))
    
    dd = df.loc[ (df['first'] < y+relativedelta(months=+1)) & (df['last'] > y) & (df['site']==x) & (df['method']=='streamed')]
    rd = dd['referenceDesignator'].unique()
    output_streamed = output_streamed.set_value(x,y,len(rd))

# Remove months where expected data should be 0
output_telemetered[output_ops==0]=0
output_recovered[output_ops==0]=0
output_streamed[output_ops==0]=0


#-------------------------
# Output data
#output.to_csv('test_output.csv',header=True)
writer = pd.ExcelWriter('stats_output.xlsx')
output_ops.to_excel(writer,'Operational')
output_telemetered.to_excel(writer,'Telemetered')
output_recovered.to_excel(writer,'Recovered')
output_streamed.to_excel(writer,'Streamed')
writer.save()

print datetime.now() - startTime