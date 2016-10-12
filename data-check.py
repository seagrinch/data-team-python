#!/usr/bin/env python
# OOI Data Team 
# Script to compare deployments with Cassandara particles
# Written by Sage, 10/10/16

import pprint
import glob
import csv
import pandas as pd
import netCDF4 as nc


def main():
  """Main function for command line execution"""

  # Read in deployment data
  file_mask = "repos/asset-management/deployment/*.csv"
  file_list = glob.glob(file_mask)
  df_from_each_file = (pd.read_csv(f) for f in file_list)
  deployments = pd.concat(df_from_each_file, ignore_index=True)
 
  # Read in Cassandra data csv as dataframe
  #cass = pd.read_csv('stats_data/partition_metadata_20161007.csv')
  cass = pd.read_json('stats_data/partition_metadata_20161012.json')

  # Select only the columns we need
  deployments = deployments[['Reference Designator', 'deploymentNumber', 'startDateTime', 'stopDateTime']]
  cass = cass[['referenceDesignator','method','first','count']]
   
  # Convert time
  deployments['start_time'] = pd.to_datetime(deployments['startDateTime'])
  deployments['end_time'] = pd.to_datetime(deployments['stopDateTime'])
  deployments['end_time'][deployments['end_time'].isnull()] = pd.datetime.today()
  
  time_units = 'seconds since 1900-01-01'
  cass = cass[cass['first'] < 1e+10] #Hack to remove bad ZPLSC data
  cass = cass[cass['first'] > 1e+8] #Hack to remove bad times
  cass['first'] = nc.num2date(cass['first'], time_units)

  print 'Iterating over '+ str(len(deployments)) +' Deployments'

  for index, row in deployments.iterrows():
    print index
    deployments.loc[index, "telemetered"] = cass[ (cass['first'] > row['start_time']) & (cass['first'] < row['end_time']) & (cass['referenceDesignator'] == row['Reference Designator']) & (cass['method'] == 'telemetered') ]['count'].sum()
    deployments.loc[index, "streamed"] = cass[ (cass['first'] > row['start_time']) & (cass['first'] < row['end_time']) & (cass['referenceDesignator'] == row['Reference Designator']) & (cass['method'] == 'streamed') ]['count'].sum()
    deployments.loc[index, "recovered"] = cass[ (cass['first'] > row['start_time']) & (cass['first'] < row['end_time']) & (cass['referenceDesignator'] == row['Reference Designator']) & (cass['method'].isin(['recovered', 'recovered_cspp', 'recovered_host', 'recovered_inst', 'recovered_wfp'])) ]['count'].sum()

  # Export the final dataset
  deployments.to_csv('deployment_cassandra.csv')

  #   pp = pprint.PrettyPrinter(indent=4)
  #   pp.pprint(df)


# Run main function when in comand line mode        
if __name__ == '__main__':
  main()
