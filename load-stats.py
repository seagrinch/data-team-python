#!/usr/bin/env python
# OOI Data Team Portal
# Monthly Statistics Tools

import datateam
import argparse
import pprint
import time
import openpyxl as xl
import datetime
from dateutil import rrule


# Command Line Arguments
parser = argparse.ArgumentParser(description='OOI Data Team Portal - Statistics Tools')
parser.add_argument('-o','--option', required=True, 
  choices=['create','deployments','cassandra','opstatus'],
  help='Type of status data to load')
parser.add_argument('-y','--year',
  help='Enter a year')
parser.add_argument('-m','--month',
  help='Enter a month')
parser.add_argument('-s','--server',
  choices=['production','development'],
  default='development',
  help='Database server to use')
args = parser.parse_args()


def find(db,instrument,ym):
  """Find a stats record"""
  sql = 'reference_designator="%s" AND month="%s"' % (instrument,ym)
  result = db.select('monthly_stats',sql,'id')
  if len(result) > 0:
    return result[0]['id']
  else:
    return False


def save(db, data):
  """Save a stats record to the database"""
  columns = ['reference_designator', 'month','deployment_status','cassandra_ts','cassandra_rec','operational_status']
  data = datateam.common.remove_extraneous_columns(columns, data)
  id = find(db,data['reference_designator'],data['month'])
  if id == False:
    #data['created'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.insert('monthly_stats', data)
    print "Created: " +data['reference_designator'] +' ' +data['month']
  else:
    #data['modified'] = time.strftime('%Y-%m-%d %H:%M:%S')
    res = db.update('monthly_stats', id, data)
    #print "Updated: " +data['reference_designator'] +' ' +data['month']


def instrument_list(db):
  """Get a list of all instruments"""
  result = db.select('instruments','','reference_designator')
  if len(result) > 0:
    return result
  else:
    return False


def deployment_list(db):
  """Get a list of all deployments"""
  result = db.select('deployments','','reference_designator','start_date','stop_date')
  if len(result) > 0:
    return result
  else:
    return False


def create_stats(db):
  ym = args.year.zfill(4) + '-' + args.month.zfill(2) + '-01'
  print 'Creating statistics records for %s' % ym
  instruments = instrument_list(db)
  for instrument in instruments:
    data = {
      'reference_designator': instrument['reference_designator'], 
      'month': ym
    }
    save(db,data)


def load_deployment_status(db):
  """Load deployment status information"""
  # Remove previous deployment_status information
  res = db.update_where('monthly_stats', 1, deployment_status=None)
  
  # Load all deployments
  deployments = deployment_list(db)
  for deployment in deployments:
    # Skip non-instrument deployments
    if (len(deployment['reference_designator'])==27):
      # If instrument is currently deployed, use today's date as the end date
      if (deployment['stop_date']==None):
        deployment['stop_date'] = datetime.date.today()
      # Standardize date ranges to the beginning of the month
      start_date = datetime.date(deployment['start_date'].year,deployment['start_date'].month,1)
      end_date = datetime.date(deployment['stop_date'].year,deployment['stop_date'].month,1)
      # Loop over every month in range
      for dt in rrule.rrule(rrule.MONTHLY, dtstart=start_date, until=end_date):
        data = {
          'reference_designator': deployment['reference_designator'], 
          'month': dt.date().isoformat(),
          'deployment_status': 1
        }
        save(db,data)
    else:
      print 'SKIPPING: ' +deployment['reference_designator']


def load_cassandra_status(db):
  """Load Cassandra status information"""
  import pandas as pd
  import netCDF4 as nc
  # Remove previous cassandra_status information
  res = db.update_where('monthly_stats', 1, cassandra_ts=None, cassandra_rec=None)

  # Read in Cassandra data csv as dataframe
  # From http://ooiufs01.ooi.rutgers.edu:12576/sensor/inv/partition_metadata
  df = pd.read_json('stats_data/partition_metadata_20170210.json')
  # select only the columns we need
  df = df[['referenceDesignator','method','first','count']]
    
  # Convert time
  df = df[df['first'] < 1e+10] # Hacks to deal with bad times
  df = df[df['first'] > 1e+8]
  time_units = 'seconds since 1900-01-01'
  df['first'] = nc.num2date(df['first'], time_units)
  #df['first']= pd.to_timedelta(df['first'], unit='s') + pd.to_datetime('1900/1/1')
  
  # Merge recovered records
  df.loc[df['method'].isin(['recovered', 'recovered_cspp', 'recovered_host', 'recovered_inst', 'recovered_wfp']),'method'] = 'recovered'
  
  # Index the time variable
  df.index=df['first']
  
  # Group by month and list reference designators with data for each month
  a = df.groupby(by=[df.index.year,df.index.month,df.referenceDesignator,df.method])['count'].sum()
  for row in a.iteritems():
    year = row[0][0]
    month = row[0][1]
    refdes = row[0][2]
    method = row[0][3]
    if (year >= 2013 and year <= datetime.date.today().year):
      if (len(refdes)==27):
        rd = datateam.designators.find(db,'instruments',refdes)
        if (rd):
          data = {
            'reference_designator': refdes, 
            'month': str(year).zfill(4) + '-' + str(month).zfill(2) + '-01',
          }
          if method in ['telemetered', 'streamed']:
            data['cassandra_ts'] = row[1]
          elif method in ['recovered', 'recovered_cspp', 'recovered_host', 'recovered_inst', 'recovered_wfp']:
            data['cassandra_rec'] = row[1]
          save(db,data)
        else:
          print 'SKIPPING (refdes not found): ' +refdes +' ' +str(year) +'-' +str(month)      
      else:
        print 'SKIPPING (invalid refdes): ' +refdes +' ' +str(year) +'-' +str(month)      
    else:
      print 'SKIPPING (invalid date): ' +refdes +' ' +str(year) +'-' +str(month)


def load_operational_status(db):
  """Load Operational status information"""
  # Remove previous cassandra_status information
  res = db.update_where('monthly_stats', 1, operational_status=None)

  # Load in Data Team's operational status Excel file
  xlfile = 'stats_data/ExpectedData_20161206.xlsx'
  wb = xl.load_workbook(filename=xlfile, read_only=True, data_only=True)
  m_data = datateam.common.crawl_worksheet(wb[wb.get_sheet_names()[0]])
  moor_header = [str(x).lower().replace(" ", "_") for x in m_data[0]]
  # Iterate through 'Moorings' sheet data matrix
  for row in m_data[1:]:  # Skip the first row, because all cal sheets have headers
    for jj in range(4,len(moor_header)):
      data = {
        'reference_designator': row[3], 
        'month': moor_header[jj][:10],
        'operational_status': row[jj]
      }
      save(db,data)


def main():
  """Main function for command line execution"""
  db = datateam.MysqlPython()
  db.load_config(args.server)
  if args.option =="create":
    create_stats(db)
  elif args.option=="deployments":
    load_deployment_status(db)
  elif args.option=="cassandra":
    load_cassandra_status(db)
  elif args.option=="opstatus":
    load_operational_status(db)


# Run main function when in comand line mode        
if __name__ == '__main__':
  main()
