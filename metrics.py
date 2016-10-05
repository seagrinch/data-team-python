#!/usr/bin/env python

import pandas as pd
import netCDF4 as nc
import datetime
import pprint

def convert_year(row):
  return row['first'].year

def convert_month(row):
  return row['first'].month

# read in csv as data frame
df = pd.read_csv('partition_metadata_20160607.csv')

# create delta between first and last date
df['delta'] = df['last'] - df['first']

# select only the columns we need
df = df[['refdes','first','count']]

# convert time
time_units = 'seconds since 1900-01-01'
df['first'] = nc.num2date(df['first'], time_units)
df['year'] = df.apply(lambda row: convert_year(row),axis=1)
df['month'] = df.apply(lambda row: convert_month(row),axis=1)

# index time variable
df.index=df['first']

# now we can call month and year from 'first'
# df.index.month
# df.index.year

# group by month and list reference designators with data for each month
a = df.groupby(by=[df.index.year,df.index.month,df.refdes])['count'].sum()
a.to_csv('test1.csv')

#b = df.groupby(pd.TimeGrouper(freq='M'))['refdes'].apply(lambda x: "{%s}" % ','.join(x))
#c = pd.groupby(df,by=[df.index.year,df.index.month]).sum()[['count']]

d = df.groupby(['year','month','refdes'], as_index=False)['count'].sum()
d.to_csv('test2.csv')


# pp = pprint.PrettyPrinter(depth=6)
# 
# for x in a:
#   pp.pprint(x)