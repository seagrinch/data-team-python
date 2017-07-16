#!/usr/bin/env python
# OOI Data Team Portal
# Compare instrument lists
# Written by Sage 6/19/17
# Reference: https://www.quora.com/Python-How-can-I-compare-two-lists-in-CSV-files

import pandas as pd
from dateutil.relativedelta import relativedelta
from datetime import datetime

startTime = datetime.now()

#-------------------------
# First, load in master Instrument Streams list
filename = 'InstrumentStreamsAll_20170620.csv'
print 'Loading: ' + filename 
df1 = pd.read_csv(filename)
rd1 = df1['reference_designator'].unique()

#-------------------------
# Second, load in Operational Status
xlfile = 'ExpectedData_20170621.xlsx'
print 'Loading: ' + xlfile 
df2 = pd.read_excel(xlfile, sheetname='refdes2.csv')
rd2 = df2['reference_designator'].unique()

# #-------------------------
# # Compare Lists 1 & 2
# only_a = [pid for pid in rd1 if not pid in rd2]
# only_b = [pid for pid in rd2 if not pid in rd1]
# in_both = [pid for pid in rd1 if pid in rd2]
# 
# writer = pd.ExcelWriter('check_output.xlsx')
# pd.Series(only_a,name="reference_designator").to_excel(writer,'Only InstrumentStream')
# pd.Series(only_b,name="reference_designator").to_excel(writer,'Only ExpectedData')
# pd.Series(in_both,name="reference_designator").to_excel(writer,'In Both')
# writer.save()

#-------------------------
# Next, load in Cassandra Status
filename = 'partition_metadata_20170619.json'
print 'Loading: ' + filename 
df = pd.read_json(filename)
df = df[df['count']>1] # Remove rows with only 1 count
df = df[df['referenceDesignator'].str.len()==27] # Remove non-instruments
df = df[(df['first'] < 1e+10) & (df['first'] > 1e+8)] # Hacks to deal with bad times
df = df[(df['last'] < 1e+10) & (df['last'] > 1e+8)] # Hacks to deal with bad times
rd3 = df['referenceDesignator'].unique()

# #-------------------------
# # Compare Lists 2 & 3
# only_a = [pid for pid in rd2 if not pid in rd3]
# only_b = [pid for pid in rd3 if not pid in rd2]
# in_both = [pid for pid in rd2 if pid in rd3]
# 
# writer = pd.ExcelWriter('check_output2.xlsx')
# pd.Series(only_a,name="reference_designator").to_excel(writer,'Only ExpectedData')
# pd.Series(only_b,name="reference_designator").to_excel(writer,'Only Cassandra')
# pd.Series(in_both,name="reference_designator").to_excel(writer,'In Both')
# writer.save()

#-------------------------
# Compare All 3 Lists
s1=set(rd1)
s2=set(rd2)
s3=set(rd3)

only1 = s1 - s2 - s3
only2 = s2 - s1 - s3
only3 = s3 - s1 - s2
only12 = (s1 & s2) - s3
only23 = (s2 & s3) - s1
only31 = (s3 & s1) - s2
all3 = s1 & s2 & s3

# Output file
writer = pd.ExcelWriter('check_output3.xlsx')
pd.Series(list(only1),name="reference_designator").to_excel(writer,'Only Database')
pd.Series(list(only2),name="reference_designator").to_excel(writer,'Only ExpectedData')
pd.Series(list(only3),name="reference_designator").to_excel(writer,'Only Cassandra')
pd.Series(list(only12),name="reference_designator").to_excel(writer,'Missing in Cassandra')
pd.Series(list(only23),name="reference_designator").to_excel(writer,'Missing in Database')
pd.Series(list(only31),name="reference_designator").to_excel(writer,'Missing in ExpectedData')
pd.Series(list(all3),name="reference_designator").to_excel(writer,'In All 3')
writer.save()

#-------------------------
# Print Elapsed Time
print "Elapsed time: " + str(datetime.now() - startTime)
