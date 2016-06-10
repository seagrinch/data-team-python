#!/usr/bin/env python
# OOI Datateam Import - Load Data Script

import datateam
import argparse

# Command Line Arguments
parser = argparse.ArgumentParser(description='OOI Data Team Portal Importer')
parser.add_argument('-o','--option',
  choices=['regions', 'sites','nodes','instruments',
    'instrument_classes','instrument_models',
    'assets','deployments','preload','data_streams'],
  help='Type of data to load')
args = parser.parse_args()


def main():
  """Main function for command line execution"""
  db = datateam.MysqlPython()
  db.load_config()
  if args.option =="regions":
    datateam.designators.load_regions(db)
  elif args.option=="sites":
    datateam.designators.load_sites(db)
  elif args.option=="nodes":
    datateam.designators.load_nodes(db)
  elif args.option=="instruments":
    datateam.designators.load_instruments(db)
  elif args.option=="instrument_classes":
    datateam.instrument_class.load(db)
  elif args.option=="instrument_models":
    datateam.instrument_model.load(db)
  elif args.option=="assets":
    datateam.assets.load(db)
  elif args.option=="deployments":
    datateam.deployments.load(db)
  elif args.option=="preload":
    datateam.preload.load(db)
  elif args.option=="data_streams":
    datateam.data_streams.load(db)


# Run main function when in comand line mode        
if __name__ == '__main__':
  main()
