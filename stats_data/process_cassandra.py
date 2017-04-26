#!/usr/bin/env python
# OOI Data Team Portal
# Process Cassandra Stats

import pandas as pd
import netCDF4 as nc

filename = 'partition_metadata_20170315.json'

# Read in Cassandra data csv as dataframe
print 'Processing: ' + filename 
df = pd.read_json(filename)

# Select only the columns we need
df = df[['referenceDesignator','method','stream','first','count']]
  
# Convert time
df = df[df['first'] < 1e+10] # Hacks to deal with bad times
df = df[df['first'] > 1e+8]
time_units = 'seconds since 1900-01-01'
df['first'] = nc.num2date(df['first'], time_units)
# df['first']= pd.to_timedelta(df['first'], unit='s') + pd.to_datetime('1900/1/1') #old way

# Merge recovered records
# df.loc[df['method'].isin(['recovered', 'recovered_cspp', 'recovered_host', 'recovered_inst', 'recovered_wfp']),'method'] = 'recovered'

# Index the time variable
df.index=df['first']

# Group by month and list reference designators with data for each month
a = df.groupby(by=[df.index.year,df.index.month,df.referenceDesignator,df.method,df.stream])['count'].sum()
print a.head(25)

a.to_csv('test.csv',header=True)

# for row in a.iteritems():
#   year = row[0][0]
#   month = row[0][1]
#   refdes = row[0][2]
#   method = row[0][3]
#   stream = row[0][4]
#   if (year >= 2013 and year <= datetime.date.today().year):
#     if (len(refdes)==27):
#       rd = datateam.designators.find(db,'instruments',refdes)
#       if (rd):
#         data = {
#           'reference_designator': refdes, 
#           'month': str(year).zfill(4) + '-' + str(month).zfill(2) + '-01',
#         }
#         if method in ['telemetered', 'streamed']:
#           data['cassandra_ts'] = row[1]
#         elif method in ['recovered', 'recovered_cspp', 'recovered_host', 'recovered_inst', 'recovered_wfp']:
#           data['cassandra_rec'] = row[1]
#         save(db,data)
#       else:
#         print 'SKIPPING (refdes not found): ' +refdes +' ' +str(year) +'-' +str(month)      
#     else:
#       print 'SKIPPING (invalid refdes): ' +refdes +' ' +str(year) +'-' +str(month)      
#   else:
#     print 'SKIPPING (invalid date): ' +refdes +' ' +str(year) +'-' +str(month)

